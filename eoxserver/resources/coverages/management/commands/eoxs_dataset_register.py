#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#          Martin Paces <martin.paces@eox.at>
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

from optparse import make_option

from django.core.management import call_command
from django.core.management.base import CommandError, BaseCommand
from django.utils.dateparse import parse_datetime
from django.contrib.gis import geos

from eoxserver.core import env
from eoxserver.backends.cache import CacheContext
from eoxserver.resources.coverages.registration.component import (
    RegistratorComponent
)
from eoxserver.resources.coverages.management.commands import (
    CommandOutputMixIn, _variable_args_cb, nested_commit_on_success
)


def _variable_args_cb_list(option, opt_str, value, parser):
    """ Helper function for optparse module. Allows variable number of option
        values when used as a callback.
    """
    args = []
    for arg in parser.rargs:
        if not arg.startswith('-'):
            args.append(arg)
        else:
            del parser.rargs[:len(args)]
            break
    if not getattr(parser.values, option.dest):
        setattr(parser.values, option.dest, [])

    getattr(parser.values, option.dest).append(args)


class Command(CommandOutputMixIn, BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-i", "--identifier", "--coverage-id", dest="identifier",
            action="store", default=None,
            help=("Override identifier.")
        ),
        make_option("-d", "--data", dest="data",
            action="callback", callback=_variable_args_cb_list, default=[],
            help=("Add a data item to the dataset. Format is: "
                  "[storage_type:url] [package_type:location]* format:location"
                 )
        ),
        make_option("-s", "--semantic", dest="semantics",
            action="callback", callback=_variable_args_cb, default=None,
            help=("Optional band semantics. If given, one band "
                  "semantics 'band[*]' must be present for each '--data' "
                  "option.")
        ),
        make_option("-m", "--meta-data", dest="metadata",
            action="callback", callback=_variable_args_cb_list, default=[],
            help=("Optional. [storage_type:url] [package_type:location]* "
                  "format:location")
        ),
        make_option("-r", "--range-type", dest="range_type_name",
            help=("Mandatory. Name of the stored range type. ")
        ),

        make_option("-e", "--extent", dest="extent",
            action="store", default=None,
            help=("Override extent. Comma separated list of "
                  "<minx>,<miny>,<maxx>,<maxy>.")
        ),

        make_option("--size", dest="size",
            action="store", default=None,
            help=("Override size. Comma separated list of <size-x>,<size-y>.")
        ),

        make_option("--srid", dest="srid",
            action="store", default=None,
            help=("Override SRID. Integer number.")
        ),

        make_option("-p", "--projection", dest="projection",
            action="store", default=None,
            help=("Override projection.")
        ),

        make_option("-f", "--footprint", dest="footprint",
            action="store", default=None,
            help=("Override footprint. Must be supplied as WKT Polygons or "
                  "MultiPolygons.")
        ),

        make_option("--begin-time", dest="begin_time",
            action="store", default=None,
            help=("Override begin time. Format is ISO8601 datetime strings.")
        ),

        make_option("--end-time", dest="end_time",
            action="store", default=None,
            help=("Override end time. Format is ISO8601 datetime strings.")
        ),

        make_option("--coverage-type", dest="coverage_type",
            action="store", default=None,
            help=("The actual coverage type.")
        ),

        make_option("--visible", dest="visible",
            action="store_true", default=False,
            help=("Set the coverage to be 'visible', which means it is "
                  "advertised in GetCapabilities responses.")
        ),

        make_option("--collection", dest="collection_ids",
            action='callback', callback=_variable_args_cb, default=None,
            help=("Optional. Link to one or more collection(s).")
        ),

        make_option('--ignore-missing-collection',
            dest='ignore_missing_collection',
            action="store_true", default=False,
            help=("Optional. Proceed even if the linked collection "
                  "does not exist. By default, a missing collection "
                  "will result in an error.")
        ),

        make_option("--replace",
            action="store_true", default=False,
            help=("Optional. If the coverage with the given identifier already "
                  "exists, replace it. Without this flag, this would result in "
                  "an error.")
        ),

        make_option("--scheme",
            action="store", default="GDAL",
            help=("Optional. How the input files shall be treated and "
                  "registered. Default is the 'GDAL' scheme.")
        )
    )

    args = (
        "-d [<storage>:][<package>:]<location> [-d ... ] "
        "-r <range-type-name> "
        "[-m [<storage>:][<package>:]<location> [-m ... ]] "
        "[-s <semantic> [-s <semantic>]] "
        "[--identifier <identifier>] "
        "[-e <minx>,<miny>,<maxx>,<maxy>] "
        "[--size <size-x> <size-y>] "
        "[--srid <srid> | --projection <projection-def>] "
        "[--footprint <footprint-wkt>] "
        "[--begin-time <begin-time>] [--end-time <end-time>] "
        "[--coverage-type <coverage-type-name>] "
        "[--visible] [--collection <collection-id> [--collection ... ]] "
        "[--ignore-missing-collection] "
        "[--replace]"
    )

    help = """
        Registers a Dataset.
        A dataset is a collection of data and metadata items. When beeing
        registered, as much metadata as possible is extracted from the supplied
        (meta-)data items. If some metadata is still missing, it needs to be
        supplied via the specific override options.

        By default, datasets are not "visible" which means that they are not
        advertised in the GetCapabilities sections of the various services.
        This needs to be overruled via the `--visible` switch.

        The registered dataset can optionally be directly inserted one or more
        collections.
    """

    @nested_commit_on_success
    def handle(self, *args, **kwargs):
        with CacheContext() as cache:
            self.handle_with_cache(cache, *args, **kwargs)

    def handle_with_cache(self, cache, *args, **kwargs):
        scheme = kwargs['scheme']
        for registrator in RegistratorComponent(env).registrators:
            if registrator.scheme == scheme:
                break
        else:
            raise CommandError("No registrator for scheme '%s' found." % scheme)

        datas = kwargs["data"]
        semantics = kwargs.get("semantics")
        metadatas = kwargs["metadata"]
        replace = kwargs['replace']

        print datas, semantics, metadatas

        try:
            dataset, replaced = registrator.register(
                datas, semantics, metadatas, self._get_overrides(**kwargs),
                replace, cache
            )
            if replace and replaced:
                self.print_msg(
                    "Dataset with ID '%s' replaced sucessfully."
                    % (dataset.identifier)
                )
            elif replace:
                self.print_wrn(
                    "Could not replace Dataset with ID '%s' but inserted it."
                    % (dataset.identifier)
                )
            else:
                self.print_msg(
                    "Dataset with ID '%s' inserted sucessfully."
                    % (dataset.identifier)
                )

            # link with collection(s)
            if kwargs["collection_ids"]:
                ignore_missing_collection = kwargs["ignore_missing_collection"]
                call_command("eoxs_collection_link",
                    collection_ids=kwargs["collection_ids"],
                    add_ids=[dataset.identifier],
                    ignore_missing_collection=ignore_missing_collection
                )
        except Exception as e:
            self.print_traceback(e, kwargs)
            raise CommandError(
                "Dataset registration failed: %s" % e
            )

    def _get_overrides(self, identifier=None, size=None, extent=None,
                       begin_time=None, end_time=None, footprint=None,
                       projection=None, coverage_type=None, srid=None,
                       range_type_name=None, **kwargs):

        overrides = {}

        if coverage_type:
            overrides["coverage_type"] = coverage_type

        if identifier:
            overrides["identifier"] = identifier

        if extent:
            overrides["extent"] = map(float, extent.split(","))

        if size:
            overrides["size"] = map(int, size.split(","))

        if begin_time:
            overrides["begin_time"] = parse_datetime(begin_time)

        if end_time:
            overrides["end_time"] = parse_datetime(end_time)

        if range_type_name:
            overrides["range_type_name"] = range_type_name

        if footprint:
            footprint = geos.GEOSGeometry(footprint)
            if footprint.hasz:
                raise CommandError(
                    "Invalid footprint geometry! 3D geometry is not supported!"
                )
            if footprint.geom_type == "MultiPolygon":
                overrides["footprint"] = footprint
            elif footprint.geom_type == "Polygon":
                overrides["footprint"] = geos.MultiPolygon(footprint)
            else:
                raise CommandError(
                    "Invalid footprint geometry type '%s'!"
                    % (footprint.geom_type)
                )

        if projection:
            try:
                overrides["projection"] = int(projection)
            except ValueError:
                overrides["projection"] = projection

        elif srid:
            try:
                overrides["projection"] = int(srid)
            except ValueError:
                pass

        return overrides
