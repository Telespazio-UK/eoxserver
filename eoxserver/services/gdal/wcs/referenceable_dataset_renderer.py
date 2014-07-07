#-------------------------------------------------------------------------------
# $Id$
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2013 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------


from os.path import splitext, abspath
from datetime import datetime
from uuid import uuid4

from django.contrib.gis.geos import GEOSGeometry

from eoxserver.core import Component, implements
from eoxserver.core.util.rect import Rect
from eoxserver.backends.access import connect
from eoxserver.contrib import gdal, osr
from eoxserver.contrib.vrt import VRTBuilder
from eoxserver.resources.coverages import models
from eoxserver.services.ows.version import Version
from eoxserver.services.subset import Subsets
from eoxserver.services.result import ResultFile, ResultBuffer
from eoxserver.services.ows.wcs.interfaces import WCSCoverageRendererInterface
from eoxserver.services.ows.wcs.v20.encoders import WCS20EOXMLEncoder
from eoxserver.services.exceptions import (
    RenderException, OperationNotSupportedException
)
from eoxserver.processing.gdal import reftools


class GDALReferenceableDatasetRenderer(Component):
    implements(WCSCoverageRendererInterface)

    versions = (Version(2, 0),)

    def supports(self, params):
        return (
            issubclass(params.coverage.real_type, models.ReferenceableDataset)
            and params.version in self.versions
        )


    def render(self, params):
        # get the requested coverage, data items and range type.
        coverage = params.coverage
        data_items = coverage.data_items.filter(semantic__startswith="bands")
        range_type = coverage.range_type

        subsets = Subsets(params.subsets)

        # GDAL source dataset. Either a single file dataset or a composed VRT 
        # dataset.
        src_ds = self.get_source_dataset(
            coverage, data_items, range_type
        )

        # retrieve area of interest of the source image according to given 
        # subsets
        src_rect, dst_rect = self.get_source_and_dest_rect(src_ds, subsets)

        # deduct "native" format of the source image
        native_format = data_items[0].format if len(data_items) == 1 else None

        # get the requested image format, which defaults to the native format
        # if available
        frmt = params.format or native_format

        if not frmt:
            raise RenderException("No format specified.", "format")


        # perform subsetting either with or without rangesubsetting
        subsetted_ds = self.perform_subset(
            src_ds, range_type, src_rect, dst_rect, params.rangesubset
        )

        # encode the processed dataset and save it to the filesystem
        out_ds, out_driver = self.encode(subsetted_ds, frmt)

        driver_metadata = out_driver.GetMetadata_Dict()
        mime_type = driver_metadata.get("DMD_MIMETYPE")
        extension = driver_metadata.get("DMD_EXTENSION")

        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_base = "%s_%s" % (coverage.identifier, time_stamp)

        result_set = [
            ResultFile(
                path, mime_type, "%s.%s" % (filename_base, extension),
                ("cid:coverage/%s" % coverage.identifier) if i == 0 else None
            ) for i, path in enumerate(out_ds.GetFileList())
        ]

        if params.mediatype.startswith("multipart"):
            reference = "cid:coverage/%s" % result_set[0].filename
            
            if subsets.has_x and subsets.has_y:
                footprint = GEOSGeometry(reftools.get_footprint_wkt(out_ds))
                if not subsets.xy_srid:
                    extent = footprint.extent
                else:
                    extent = subsets.xy_bbox
                encoder_subset = (
                    subsets.xy_srid, src_rect.size, extent, footprint
                )
            else:
                encoder_subset = None

            encoder = WCS20EOXMLEncoder()
            content = encoder.serialize(
                encoder.encode_referenceable_dataset(
                    coverage, range_type, reference, mime_type, encoder_subset
                )
            )
            result_set.insert(0, ResultBuffer(content, encoder.content_type))

        return result_set


    def get_source_dataset(self, coverage, data_items, range_type):
        if len(data_items) == 1:
            return gdal.OpenShared(abspath(connect(data_items[0])))
        else:
            vrt = VRTBuilder(
                coverage.size_x, coverage.size_y,
                vrt_filename=temp_vsimem_filename()
            )

            # sort in ascending order according to semantic
            data_items = sorted(data_items, key=(lambda d: d.semantic))

            gcps = []
            compound_index = 0
            for data_item in data_items:
                path = abspath(connect(data_item))

                # iterate over all bands of the data item
                for set_index, item_index in self._data_item_band_indices(data_item):
                    if set_index != compound_index + 1: 
                        raise ValueError
                    compound_index = set_index

                    band = range_type[set_index]
                    vrt.add_band(band.data_type)
                    vrt.add_simple_source(
                        set_index, path, item_index
                    )

            return vrt.dataset


    def get_source_and_dest_rect(self, dataset, subsets):
        size_x, size_y = dataset.RasterXSize, dataset.RasterYSize
        image_rect = Rect(0, 0, size_x, size_y)

        if not subsets:
            subset_rect = image_rect

        # pixel subset
        elif subsets.xy_srid is None: # means "imageCRS"
            minx, miny, maxx, maxy = subsets.xy_bbox

            minx = int(minx) if minx is not None else image_rect.offset_x
            miny = int(miny) if miny is not None else image_rect.offset_y
            maxx = int(maxx) if maxx is not None else image_rect.upper_x
            maxy = int(maxy) if maxy is not None else image_rect.upper_y

            subset_rect = Rect(minx, miny, maxx-minx+1, maxy-miny+1)

        # subset in geographical coordinates
        else:
            vrt = VRTBuilder(*image_rect.size)
            vrt.copy_gcps(dataset)

            options = reftools.suggest_transformer(dataset)

            subset_rect = reftools.rect_from_subset(
                vrt.dataset, subsets.xy_srid, *subsets.xy_bbox, **options
            )

        # check whether or not the subsets intersect with the image
        if not image_rect.intersects(subset_rect):
            raise RenderException("Subset outside coverage extent.", "subset")

        src_rect = subset_rect #& image_rect # TODO: why no intersection??
        dst_rect = src_rect - subset_rect.offset

        return src_rect, dst_rect


    def perform_subset(self, src_ds, range_type, subset_rect, dst_rect, 
                       rangesubset=None):
        vrt = VRTBuilder(*subset_rect.size)

        input_bands = list(range_type)

        # list of band indices/names. defaults to all bands
        if rangesubset:
            subset_bands = rangesubset.get_band_indices(range_type, 1)
        else:
            subset_bands = xrange(1, len(range_type) + 1)

        for dst_index, src_index in enumerate(subset_bands, start=1):
            input_band = input_bands[src_index-1]
            vrt.add_band(input_band.data_type)
            vrt.add_simple_source(
                dst_index, src_ds, src_index, subset_rect, dst_rect
            )

        vrt.copy_metadata(src_ds)
        vrt.copy_gcps(src_ds, subset_rect)

        return vrt.dataset


    def encode(self, dataset, format):
        #format, options = None
        options = {}
        options = [
            ("%s=%s" % key, value) for key, value in (options or {}).items()
        ]

        path = "/tmp/%s" % uuid4().hex
        out_driver = gdal.GetDriverByName("GTiff")
        return out_driver.CreateCopy(path, dataset, True, options), out_driver


def index_of(iterable, predicate, default=None, start=1):
    for i, item in enumerate(iterable, start):
        if predicate(item):
            return i
    return default

def temp_vsimem_filename():
    return "/vsimem/%s" % uuid4().hex
