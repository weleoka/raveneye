"""
# Copyright (c) 2017 Kai Weeks.
# See LICENSE for details.

Module handling requests/queries and responses/replies regarding saildocs service.
"""

import ravencore.main.config as raven_conf
from ravencore.utils.helpers import merge_two_dicts

from latlon.latlon.latlon import Longitude, Latitude, LatLon


class Saildocs_query:
    """
    Class representing a query to saildocs weather service.
    """

    def __init__(self, user_instance, grib_instance):
        """
        Constructor for class.

        parameters:
            user_instance: obj. The user. # Not currently used.
            grib_instance: obj. The grib.

        return:
            void
        """
        self.user_instance = user_instance
        self.grib_instance = grib_instance

        self.query_string = None # The query, ready for sending to saildocs.

        self.build_query_string()


    def build_query_string(self):
        """
        Format the grib attributes into query string.

        Sail grib uses the request string as follows:

        gfs:40N,60N,140W,120W|1.0,1.0|6,12..48|WIND

        parameters:

        returns:
            void.
        """

        #query_string = "gfs:%s%s,%s%s,%s%s,%s%s|%s,%s..%s|%s"
        # q uery_string = self.grib
        """
        u_po = self.user_instance.position
        pos = LatLon(u_po['lat'], u_po['lon'])  
        workable = pos.to_string('%d%H') # d{1,3}W/E/N/S    
        print("\n Formatted position string: %s%s\n" % (workable))
        """
        i = 0
        g = self.grib_instance

        qstr = ['send ',
            g.model,
            ':',
            Latitude(g.latmax).to_string('%d%H'),
            ',',
            Latitude(g.latmin).to_string('%d%H'),
            ',',
            Longitude(g.lonmax).to_string('%d%H'),
            ',',
            Longitude(g.lonmin).to_string('%d%H'),
            '|',
            g.resolution,
            ',',
            g.resolution,
            '|',
            g.timestep,
            ',',
            g.timestep + g.timestep,
            '..',
            g.forecast_length,
            '|',
        ]
        
        for layer in g.layers:
            i += 1
            qstr.append(layer)

            if i < len(g.layers):
                qstr.append(',')

        self.query_string = ''.join(str(x) for x in qstr)


    def build_request(self):
        """
        Make a request data structure.

        parameters:

        returns:
            dict. The request dictionary.
        """
        raven_system = raven_conf.userdb.get('user1')

        mail = {
            'sender': "%s <%s>" % (raven_system['name'], raven_system['email']),
            'to': 'query@saildocs.com',
            'subject': '%s: day %s' % (self.user_instance.id, 1),
            'text': self.query_string,
        }
        
        tmpdict = merge_two_dicts(raven_conf.raven_job['mail'], mail)
        
        req = {
            'userid': 'user1', # The raven system is making the request on behalf of real user.
            'request_carrier': 'mail',
            'mail': tmpdict
        }

        return merge_two_dicts(raven_conf.raven_job, req)

        


       





class Saildocs_response():
    pass