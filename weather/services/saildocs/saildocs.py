"""
# Copyright (c) 2017 Kai Weeks.
# See LICENSE for details.

Module handling requests/queries and responses/replies regarding Raven saildocs service.
"""



from latlon.latlon.latlon import Longitude, Latitude, LatLon


class Saildocs_query:
    """
    Class representing a query to saildocs weather service.
    """

    def __init__(self, grib_instance):
        """
        Constructor for class.

        parameters:
            grib_instance: obj. The grib.

        return:
            void
        """
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


    def build_job_parameters(self):
        """
        Make a job data structure.

        parameters:

        returns:
            dict. The job dictionary.
        """

        req = {
            'request_carrier': 'mail',
            'mail_parameters': {
                'to': 'query@saildocs.com',
                'text': self.query_string,
            },
        }

        return req

        


       





class Saildocs_response():
    pass