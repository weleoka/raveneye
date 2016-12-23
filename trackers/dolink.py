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
import re
import json

from ravencore.utils.exceptions import *

class Dolink:
    """
    Class representing the Dolink tracker.
    """

    def __init__(self, parameters):
        """
        Constructor for class.

        parameters:
            parameters: dict. Dolink parameters.

        return:
            void
        """

        self.type = 'dolink'
        self.debug = parameters['debug']
        self.address = parameters['address']
        self.http_headers = parameters['http_headers']

        if parameters['type'] != self.type:
            raise("Incorrect tracker type.")

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
        self.page_html_raw = None # The HTML from tracker.


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
                pass # DEBUG. Dont send requests!

                self.site_data = json.loads(self.page.text)

            except json.decoder.JSONDecodeError:

                raise RavenException("Dolink tracker; unable to parse JSON object.")


            tmp = self.site_data.get('markers')[0]
            rcvd_pos = tmp.get('position')

        else:
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

        return self.position










    def parse_site_html(self):
        """ DEPRECIATED
        Parse html document to gather required data.

        parameters:

        returns:
            position: string. The position data.
            updated: string. The positions time stamp.
        """
        # Hunt the web page for what we need.
        #position_raw = self.html_raw.xpath(self.position_xpath)
        #updated_raw = self.html_raw.xpath(self.updated_xpath)

        # Keep the old data.
        self.position_old = self.position
        self.updated_old = self.updated

        # Update object attributes with new data.
        #self.position = self.parse_position_string(position_raw)
        #self.updated = self.parse_updated_string(updated_raw)


    def parse_updated_string(self, updated_str):
        """ DEPRECIATED
        Parse updated string to get usable data.

        parameters:
            updated_str: string. The raw updated string from HTML document.
                # Màj: 18/12 - 18:19:37 to # "DDMMYY:HHMM" (proposed)

        returns:
            void.
        """
        self.position = "I dont care right now: " + updated_str# "DDMMYY:HHMM"


    def parse_position_string(self, position_str):
        """ DEPRECIATED
        Parse position string to get usable data.

        parameters:
            position_str: string. The raw position string from HTML document.
                # Lat: 15° 52' 05" N -&nbsp;Lon: 61° 35' 06" W

        returns:
            lat: dict. The latitude.
            lon: dict. The longitude.
        """

        pattern = re.compile('''
            (               # Parenthesis keep the match when string is split.
                \d{1,3}     # A number between 1 and 3 digits long.
                |           # OR
                \s[A-Z]\s   # Space, single letter(uppercase), space.
            )
        ''', re.VERBOSE)
        #-['Lat: ', '15', '° ', '52', "' ", '05', '"', ' N ', '-&nbsp;Lon: ', '61', '° ', '35', "' ", '06', '" W']
        # tmp_arr = re.match(pattern, position_str)
        # print("Different: %s" % (tmp_arr))
        print(position_str)
        position_str[0].split('-&nbsp;')
        raw_lat_arr = re.split(pattern, position_str[0])
        raw_lon_arr = re.split(pattern, position_str[1])

        for item in raw_lat_arr:
            item.strip()

        for item in raw_lon_arr:
            item.strip()

        print(tmp_arr)
        print(raw_lat_arr)
        print(raw_lon_arr)

        self.position = "%s %s %s %s;%s %s %s %s" % (
            raw_lat_arr[1],
            raw_lat_arr[3],
            raw_lat_arr[5],
            raw_lat_arr[7],
            raw_lon_arr[1],
            raw_lon_arr[3],
            raw_lon_arr[5],
            raw_lon_arr[7]
        )



def main():
    pass

if __name__ == '__main__': main()