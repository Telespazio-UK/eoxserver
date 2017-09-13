#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2011 EOX IT Services GmbH
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

from os.path import join
from uuid import uuid4
import re

from eoxserver.contrib import vsi, vrt, mapserver, gdal
from eoxserver.resources.coverages import models
from eoxserver.processing.gdal import reftools


class MultiFileConnector(object):
    """ Connects multiple files containing the various bands of the coverage
        with the given layer. A temporary VRT file is used as abstraction for
        the different band files.
    """

    def supports(self, coverage, data_items):
        # TODO: better checks
        return (
            len(data_items) > 1 and all(
                map(lambda d: d.semantic.startswith("bands"), data_items)
            )
        )

    def connect(self, coverage, data_items, layer, options):
        path = join("/vsimem", uuid4().hex)
        range_type = coverage.range_type
        num_bands = len(coverage.range_type)

        vrt_builder = vrt.VRTBuilder(
            coverage.size_x, coverage.size_y, vrt_filename=path
        )

        bands_re = re.compile(r"bands\[(\d+)(,\d+)?\]")

        for data_item in sorted(data_items, key=lambda d: d.semantic):
            start, end = bands_re.match(data_item.semantic).groups()
            start = int(start)
            end = int(end) if end is not None else None
            if end is None:
                dst_band_indices = range(start+1, start+2)
                src_band_indices = range(1, 2)
            else:
                dst_band_indices = range(start+1, end+2)
                src_band_indices = range(1, end-start+1)

            for src_index, dst_index in zip(src_band_indices, dst_band_indices):
                vrt_builder.add_band(range_type[dst_index-1].data_type)
                vrt_builder.add_simple_source(
                    dst_index,
                    #gdal.OpenShared(data_item.location),
                    data_item.location,
                    src_index
                )

        print data_items[0].location
        print gdal.OpenShared(data_items[0].location).GetGCPs()
        if isinstance(coverage, models.ReferenceableDataset):
            vrt_builder.copy_gcps(gdal.OpenShared(data_items[0].location))
            layer.setMetaData("eoxs_ref_data", path)

        layer.data = path

        #with vsi.open(path, "w+") as f:
        #    print type(vrt_builder.build())
        #    f.write(vrt_builder.build())

        del vrt_builder
        with vsi.open(path) as f:
            print f.read(100000)

        #layer.clearProcessing()
        #layer.addProcessing("SCALE_1=1,4")
        #layer.addProcessing("BANDS=2")
        #layer.offsite = mapserver.colorObj(0,0,0)

        if isinstance(coverage, models.ReferenceableDataset):
            vrt_path = join("/vsimem", uuid4().hex)
            reftools.create_rectified_vrt(path, vrt_path)
            layer.data = vrt_path
            layer.setMetaData("eoxs_ref_data", path)

            with vsi.open(vrt_path) as f:
                print f.read(100000)

        """
        # TODO!!
        if layer.metadata.get("eoxs_wrap_dateline") == "true":
            e = wrap_extent_around_dateline(coverage.extent, coverage.srid)

            vrt_path = join("/vsimem", uuid4().hex)
            ds = gdal.Open(data)
            vrt_ds = create_simple_vrt(ds, vrt_path)
            size_x = ds.RasterXSize
            size_y = ds.RasterYSize

            dx = abs(e[0] - e[2]) / size_x
            dy = abs(e[1] - e[3]) / size_y

            vrt_ds.SetGeoTransform([e[0], dx, 0, e[3], 0, -dy])
            vrt_ds = None

            layer.data = vrt_path
        """

    def disconnect(self, coverage, data_items, layer, options):
        vsi.remove(layer.data)
        vrt_path = layer.metadata.get("eoxs_ref_data")
        if vrt_path:
            vsi.remove(vrt_path)
