#!/usr/bin/env python3
# Copyright (c) 2017 Kai Weeks.
# See LICENSE for details.
"""
Instructions for scraping GPS tracker data from dolink tracker.

Functions to request web site and then use parser to gather data and return.

#-> Add tracker params for yellowbrick, spot, deLorme etc.

Tracker:
http://www.dolink.fr
<span class="mousePosition">Lat: 15° 52' 05" N -&nbsp;Lon: 61° 35' 06" W</span>
<span class="lastUpdate">Màj: 18/12 - 18:19:37</span>
"""

from lxml import html
import requests
import sys
import re
import json

import ravencore.main.config as raven_conf
from ravencore.utils.exceptions import *
import ravencore.utils.logging
import ravencore.utils.helpers


class Dolink:
    """
    Class representing the Dolink tracker.

    The DoLink will give a JSON formatted string ready for json.loads
    which saves a lot of pain with XPaths etc.

    If debug is enabled an artificial position is supplied. 
    No HTTP request has to be made. No network needed.
    """

    def __init__(self, parameters):
        """
        Constructor for class.

        parameters:
            parameters: dict. Dolink parameters.

        return:
            void
        """
        name = '.'.join([__name__, self.__class__.__name__])
        self.logger = ravencore.utils.logging.getLogger(name) 

        self.debug = parameters['debug']
        self.address = parameters['address']
        self.http_headers = parameters['http_headers']

        self.site_data = None # JSON from site.

        self.position = None # Dict containing position data.

        self.lat = None # Decimal format ex. 15.867476
        self.lon = None # Decimal format ex. -61.584935
        self.cog = None # Decimal format ex. 230.72886460781
        self.updated = None # Unix timestamp ex. 1482083016

        self.position_old = None
        self.updated_old = None

        # The Xpaths for parsing HTML from site. Depreciated.
        # self.position_xpath = '//span[@class="mousePosition"]/text()'
        # self.updated_xpath = '//span[@class="lastUpdate"]/text()'

        self.page = None # The request instance.
        # self.page_html_raw = None # The HTML from tracker. Depreciated.


    def get_position(self):
        """
        Request page with JSON object.

        Parse page.text (.content is in bytes format) JSON into python dict.

        #-> Need to screen collected data.

        parameters:

        returns:
            void.
        """
       
        if not self.debug:
            self.page = requests.get(self.address, self.http_headers)

            try:
                self.site_data = json.loads(self.page.text)

            except json.decoder.JSONDecodeError:
                self.logger.debug("Unable to update user position from Dolink tracker. (JSON decode error)")
                #raise RavenException("Dolink tracker; unable to parse JSON object.")
                return False

            tmp = self.site_data.get('markers')[0]
            rcvd_pos = tmp.get('position')
            self.logger.debug("New user position (updated: %s) from Dolink tracker." 
                % (ravencore.utils.helpers.to_utc(rcvd_pos['date'])))

        else:
            self.logger.debug("Debug mode is on. Artificial position supplied.")
            rcvd_pos = {
                    'longitude': '-61.584721',
                    'latitude': '15.870019',
                    'cap': '179.81771559233',
                    'pid': '7258849',
                    'date': '1482451584'
            }

        self.position = {
            'lat': rcvd_pos['latitude'],
            'lon': rcvd_pos['longitude'],
            'cog': rcvd_pos['cap'],
            'updated': rcvd_pos['date'],
            'pid': rcvd_pos['pid']
        }

        return True


def main():
    print("Can't run without input parameters from wrapper classes.")
    sys.exit()

if __name__ == '__main__': main()