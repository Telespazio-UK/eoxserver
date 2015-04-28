#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2015 EOX IT Services GmbH
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


from eoxserver.core import Component, ExtensionPoint
from eoxserver.core.decoders import kvp
from eoxserver.resources.coverages import models
from eoxserver.services.opensearch.interfaces import (
    SearchExtensionInterface, ResultFormatInterface
)


class OpenSearch11SearchHandler(Component):
    search_extensions = ExtensionPoint(SearchExtensionInterface)
    result_formats = ExtensionPoint(ResultFormatInterface)

    def handle(self, request, collection_id=None):
        decoder = OpenSearch11BaseDecoder(request.GET)

        if collection_id:
            qs = models.Collection.objects.get(
                identifier=collection_id
            ).eo_objects.all()
        else:
            qs = models.EOObject.objects.all()

        for search_extension in self.search_extensions:
            # get all search extension related parameters and translate the name
            # to the actual parameter name
            params = dict(
                (value[0], request.GET[key])
                for key, value in search_extension.schema.items()
                if key in request.GET
            )
            qs = search_extension.filter(qs, params)

        if decoder.start_index and not decoder.count:
            qs = qs[decoder.start_index:]
        elif decoder.start_index and decoder.count:
            qs = qs[decoder.start_index:decoder.start_index+decoder.count]
        elif decoder.count:
            qs = qs[:decoder.count]

        result_format = next(
            result_format
            for result_format in self.result_formats
            if result_format.name == decoder.format
        )

        return (
            result_format.encode(qs), result_format.mimetype
        )


def pos_int_zero(raw):
    value = int(raw)
    if value < 0:
        raise ValueError("Value is negative")
    return value


def pos_int(raw):
    value = int(raw)
    if value < 1:
        raise ValueError("Value is negative or zero")
    return value


class OpenSearch11BaseDecoder(kvp.Decoder):
    format = kvp.Parameter("format", num=1)
    start_index = kvp.Parameter("startIndex", pos_int_zero, num="?", default=0)
    count = kvp.Parameter("count", pos_int, num="?", default=None)
    output_encoding = kvp.Parameter("outputEncoding", num="?", default="UTF-8")
