#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2019 EOX IT Services GmbH
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

from eoxserver.core.util.xmltools import parse
from eoxserver.core.decoders import xml, to_dict, InvalidParameterException

from eoxserver.resources.coverages.metadata.utils.gsc import (
    NS_GSC, nsmap, GSCFormatDecoder
)


class GSCFormatExtendedDecoder(xml.Decoder):
    namespaces = nsmap

    cloud_cover = xml.Parameter("gsc:opt_metadata/gml:resultOf/opt:EarthObservationResult/opt:cloudCoverPercentage/text()", type=float, num="?")


class GSCProductMetadataReader(object):
    def test(self, obj):
        tree = parse(obj)

        tag = tree.getroot().tag if tree is not None else None
        return tree is not None and tag == NS_GSC('report')

    def read(self, obj):
        tree = parse(obj)
        if tree is not None:
            decoder = GSCFormatDecoder(tree)
            values = {
                "identifier": decoder.identifier,
                "begin_time": decoder.begin_time,
                "end_time": decoder.end_time,
                "footprint": decoder.footprint,
                "format": "gsc",
            }
            values.update(to_dict(GSCFormatExtendedDecoder(tree)))
            return values
