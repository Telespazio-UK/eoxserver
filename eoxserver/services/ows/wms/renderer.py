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


from itertools import chain

from django.db.models import Q
from django.utils.datastructures import SortedDict

from eoxserver.backends.cache import CacheContext
from eoxserver.contrib.mapserver import create_request, Map
from eoxserver.services.component import MapServerComponent, env

class WMSCapabilitiesRenderer(object):
    def render(self, request, coverages_qs, dataset_series_qs):
        ms_component = MapServerComponent(env)
        conf = CapabilitiesConfigReader(get_eoxserver_config())

        map_ = Map()
        # TODO: add all the capabilities relevant metadata

        factory_cache = {}

        for coverage in coverages_qs:
            coverage_type = coverage.real_type
            if coverage_type not in factory_cache:
                factory_cache[coverage_type] = [
                    factory
                    for factory in ms_component.layer_factories
                    if issubclass(coverage_type, factory.handles)
                ]

            for factory in factory_cache[coverage_type]:
                layer = factory.generate(coverage)

            map_.insertLayer(layer)
            # TODO meta layer via layer groups

        return map_.dispatch(r)


class WMSMapRenderer(object):
    def render(self, layer_groups, request_values, **options):
        ms_component = MapServerComponent(env)

        map_ = Map()
        map_.setMetaData("ows_enable_request", "*")
        map_.setProjection("EPSG:4326")

        group_layers = SortedDict()
        coverage_layers = []
        connector_to_layers = {}

        with CacheContext() as cache:
            for names, suffix, coverage in layer_groups.walk():
                # get a factory for the given coverage and suffix
                factory = ms_component.get_layer_factory(
                    coverage.real_type, suffix
                )
                if not factory:
                    raise "Could not find a factory for suffix '%s'" % suffix

                suffix = suffix or "" # transform None to empty string

                group_name = None
                group_layer = None

                group_name = "/" + "/".join(
                    map(lambda n: n + suffix, names[1:])
                )

                if len(names) > 1:
                    # create a group layer
                    if group_name not in group_layers:
                        group_layer = factory.generate_group(names[-1] + suffix)
                        if group_layer:
                            group_layers[group_name] = group_layer
                if not group_layer:
                    group_layer = group_layers.get(group_name)


                data_items = coverage.data_items.filter(
                    Q(semantic__startswith="bands") | Q(semantic="tileindex")
                )

                layers = factory.generate(coverage, group_layer, options)
                for layer in layers:
                    if group_name:
                        layer.setMetaData("wms_layer_group", group_name)

                    if factory.requires_connection:
                        connector = ms_component.get_connector(data_items)
                        if not connector:
                            raise ""

                        connector.connect(coverage, data_items, layer, cache)
                        connector_to_layers.setdefault(connector, []).append(
                            (coverage, data_items, layer)
                        )
                    coverage_layers.append(layer)

            for layer in chain(group_layers.values(), coverage_layers):
                old_layer = map_.getLayerByName(layer.name)
                if old_layer:
                    # remove the old layer and reinsert the new one, to 
                    # raise the layer to the top.
                    # TODO: find a more efficient way to do this
                    map_.removeLayer(old_layer.index)
                map_.insertLayer(layer)

            request = create_request(request_values)

            try:
                response = map_.dispatch(request)
                return response.content, response.content_type
            finally:
                # cleanup
                for connector, items in connector_to_layers.items():
                    for coverage, data_items, layer in items:
                        connector.disconnect(coverage, data_items, layer, cache)
