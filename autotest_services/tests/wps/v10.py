#-------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Martin Paces <martin.paces@eox.at>
#          Fabian Schindler <fabian.schindler@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2014 EOX IT Services GmbH
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

from autotest_services import testbase


#===============================================================================
# WCS 1.0 GetCapabilities
#===============================================================================

class WPS10GetCapabilitiesValidTestCase(testbase.XMLTestCase):
    def getRequest(self):
        params = "service=WPS&version=1.0.0&request=GetCapabilities"
        return (params, "kvp")

class WPS10PostGetCapabilitiesValidTestCase(testbase.XMLTestCase):
    def getRequest(self):
        params = """<wps:GetCapabilities updateSequence="u2001" service="WPS"
          xmlns:wps="http://www.opengis.net/wps/1.0"
          xmlns:ows="http://www.opengis.net/ows/1.1">
            <ows:AcceptVersions><ows:Version>1.0.0</ows:Version></ows:AcceptVersions>
          </wps:GetCapabilities>
        """
        return (params, "xml")


#===============================================================================
# WCS 1.0 DescribeProcess
#===============================================================================


class WPS10DescribeProcessValidTestCase(testbase.XMLTestCase):
    def getRequest(self):
        params = "service=WPS&version=1.0.0&request=DescribeProcess&identifier=TC00:identity:literal"
        return (params, "kvp")

class WPS10PostDescribeProcessValidTestCase(testbase.XMLTestCase):
    def getRequest(self):
        params = """<wps:DescribeProcess service="WPS" version="1.0.0"
          xmlns:wps="http://www.opengis.net/wps/1.0"
          xmlns:ows="http://www.opengis.net/ows/1.1">
            <ows:Identifier>TC00:identity:literal</ows:Identifier>
          </wps:DescribeProcess>
        """
        return (params, "xml")

class WPS10DescribeProcessValidTC01TestCase(testbase.XMLTestCase):
    def getRequest(self):
        params = "service=WPS&version=1.0.0&request=DescribeProcess&identifier=TC01:identity:bbox"
        return (params, "kvp")

class WPS10DescribeProcessValidTC02TestCase(testbase.XMLTestCase):
    def getRequest(self):
        params = "service=WPS&version=1.0.0&request=DescribeProcess&identifier=TC02:identity:complex"
        return (params, "kvp")

class WPS10DescribeProcessValidTC03TestCase(testbase.XMLTestCase):
    def getRequest(self):
        params = "service=WPS&version=1.0.0&request=DescribeProcess&identifier=TC03:image_generator:complex"
        return (params, "kvp")
