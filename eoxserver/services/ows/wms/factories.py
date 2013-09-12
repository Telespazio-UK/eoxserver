#-------------------------------------------------------------------------------
# $Id$
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


import os.path

from django.conf import settings

from eoxserver.core import Component, implements
from eoxserver.contrib.mapserver import (
    Layer, MS_LAYER_POLYGON, shapeObj, classObj, styleObj, colorObj
)
from eoxserver.resources.coverages import models, crss
from eoxserver.services.interfaces import MapServerLayerFactoryInterface


class AbstractLayerFactory(Component):
    implements(MapServerLayerFactoryInterface)
    abstract = True

    def generate(self, eo_object, group_layer, options):
        pass


    def _set_projection(self, layer, sr):
        short_epsg = "EPSG:%d" % sr.srid
        layer.setProjection(sr.proj)
        layer.setMetaData("ows_srs", short_epsg) 
        layer.setMetaData("wms_srs", short_epsg) 


class CoverageLayerFactory(AbstractLayerFactory):
    handles = (models.RectifiedDataset, models.RectifiedStitchedMosaic)
    suffix = None
    requires_connection = True

    def generate(self, eo_object, group_layer, options):
        layer = Layer(eo_object.identifier)
        layer.setMetaData("wms_extent", "%f %f %f %f" % eo_object.extent_wgs84)
        layer.setMetaData("wms_enable_request", "getcapabilities getmap getfeatureinfo")

        coverage = eo_object.cast()
        self._set_projection(layer, coverage.spatial_reference)
        # TODO: dateline...
        yield layer

    def generate_group(self, name):
        return Layer(name)


class CoverageBandsLayerFactory(AbstractLayerFactory):
    handles = (models.RectifiedDataset, models.RectifiedStitchedMosaic,)
              # TODO: ReferenceableDatasets
    suffix = "_bands"
    requires_connection = True

    def generate(self, eo_object, group_layer, options):
        name = eo_object.identifier + self.suffix
        layer = Layer(name)
        layer.setMetaData("ows_title", name)
        layer.setMetaData("wms_label", name)
        layer.addProcessing("CLOSE_CONNECTION=CLOSE")
    
        coverage = eo_object.cast()
        range_type = coverage.range_type

        req_bands = options["bands"]
        band_indices = []
        bands = []

        for req_band in req_bands:
            if isinstance(req_band, int):
                band_indices.append(req_band + 1)
                bands.append(range_type[req_band])
            else:
                for i, band in enumerate(range_type):
                    if band.name == req_band:
                        band_indices.append(i + 1)
                        bands.append(band)
                        break
                else:
                    raise "Coverage '%s' does not have a band with name '%s'." 

        if len(req_bands) in (3, 4):
            indices_str = ",".join(map(str, band_indices))
        elif len(req_bands) == 1:
            indices_str = ",".join(map(str, band_indices * 3))
        else:
            raise "Invalid number of bands requested."

        layer.setProcessingKey("BANDS", indices_str)
        layer.offsite = create_offsite_color(bands)
        
        # TODO: seems to break rendering
        #layer.setProcessingKey("SCALE", "100,200")

        yield layer
        # TODO: dateline wrapping

    def generate_group(self, name):
        return Layer(name)


class CoverageOutlinesLayerFactory(AbstractLayerFactory):
    handles = (models.RectifiedDataset, models.ReferenceableDataset,
               models.RectifiedStitchedMosaic,)
    suffix = "_outlines"
    requires_connection = False

    STYLES = (
        ("red", 255, 0, 0),
        ("green", 0, 128, 0),
        ("blue", 0, 0, 255),
        ("white", 255, 255, 255),
        ("black", 0, 0, 0),
        ("yellow", 255, 255, 0),
        ("orange", 255, 165, 0),
        ("magenta", 255, 0, 255),
        ("cyan", 0, 255, 255),
        ("brown", 165, 42, 42)
    )
    
    DEFAULT_STYLE = "red"

    def generate(self, eo_object, group_layer, options):
        # don't generate any layers, but add the footprint as feature to the 
        # group layer

        layer = group_layer
        shape = shapeObj.fromWKT(eo_object.footprint.wkt)
        shape.initValues(1)
        shape.setValue(0, eo_object.identifier)
        layer.addFeature(shape)
        layer.addProcessing("ITEMS=identifier")

        return ()


    def generate_group(self, name):
        layer = Layer(name, type=MS_LAYER_POLYGON)
        self.apply_styles(layer)

        srid = 4326
        layer.setProjection(crss.asProj4Str(srid))
        layer.setMetaData("ows_srs", crss.asShortCode(srid)) 
        layer.setMetaData("wms_srs", crss.asShortCode(srid)) 

        layer.dump = True

        layer.header = os.path.join(settings.PROJECT_DIR, "conf", "outline_template_header.html")
        layer.template = os.path.join(settings.PROJECT_DIR, "conf", "outline_template_dataset.html")
        layer.footer = os.path.join(settings.PROJECT_DIR, "conf", "outline_template_footer.html")
        
        layer.setMetaData("gml_include_items", "all")
        layer.setMetaData("wms_include_items", "all")

        layer.offsite = colorObj(0, 0, 0)

        return layer


    def apply_styles(self, layer):
        # add style info
        for name, r, g, b in self.STYLES:
            cls = classObj()
            style = styleObj()
            style.outlinecolor = colorObj(r, g, b)
            cls.insertStyle(style)
            cls.group = name
        
            layer.insertClass(cls)

        layer.classgroup = self.DEFAULT_STYLE


def create_offsite_color(bands):
    return colorObj(0,0,0)
    if len(bands) == 1:
        v = int(bands[0].nil_values.all()[0].value)
        return colorObj(v, v, v)
    elif len(bands) == 3:
        values = [int(band.nil_values.all()[0].value) for band in bands]
        return colorObj(*values)
