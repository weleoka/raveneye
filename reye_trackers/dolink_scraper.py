#!/usr/bin/env python3
# Copyright (c) 2017 Kai Weeks.
# See LICENSE for details.
"""
Instructions for scraping GPS tracker data from dolink tracker.

Functions to request web site and then use parser to gather data and return.

#-> Add tracker params for yellowbrick, spot, deLorme etc.

Tracker:
http://www.dolink.fr
'http://www.dolink.fr/carte-new/1225773'


<span class="mousePosition">Lat: 15° 52' 05" N -&nbsp;Lon: 61° 35' 06" W</span>
<span class="lastUpdate">Màj: 18/12 - 18:19:37</span>
"""

from lxml import html
import requests


def get_site_html(address = ):
    """
    Request HTML page.

    Route the HTML string of page to parse_site_html function.

    parameters:
        address: string. The page URL.

    returns:
        void.
    """
    page = requests.get(address)
    # page.content not page.text because html.fromstring implicitly expects bytes as input.
    tree = html.fromstring(page.content)

    parse_site_html(tree)


def parse_site_html(tree):
    """
    Parse html document to gather required data.

    parameters:
        tree: string. The HTML document string.

    returns:
        position: string. The position data.
        updated: string. The positions time stamp.
    """
    position = tree.xpath('//span[@class="mousePosition"]/text()')
    updated = tree.xpath('//span[@class="lastUpdate"]/text()')

    position = parse_position_string(position)
    #parse_updated_string()
    return position, updated


def parse_position_string(position_str):
    print(position_str)


def main():
    pass

if __name__ == '__main__': main()