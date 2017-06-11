"""
Class representing GRIB file.
"""

from latlon.latlon.latlon import LatLon

class Grib():
    
    def __init__(self, parameters = None):
        """
        Class constructor.

                    'model': 'gfs',
                    'subtract_from_position_lat': 10,
                    'add_to_position_lat': 10,
                    'subtract_from_position_lon': 10,
                    'add_to_position_lon': 30,
                    'resolution': '1.0',
                    'layers': ['WIND', 'MSLSP'],
                    'issue': 'latest',
                    'timestep': 6,  # 3, 6, 12, 24 hours.
                    'forecast_length': 96, # 12, 24, 48, 72, 96 (Not 36!?) hours.
        """

        [setattr(self, attr, value) for attr, value in parameters]

        # self.latmin = None
        # self.latmax = None

        # self.lonmin = None
        # self.lonmax = None

        # self.model = parameters['model']

        # self.resolution = parameters['resolution'] # 0.25, 0.5, 1.0, 2.0

        # self.issue = parameters['issue']

        # self.timestep = parameters['timestep']
        # self.forecast_length = parameters['forecast_length']

        # self.layers = parameters['layers']







    def set_forecast_region(self):
        """ NOTUSED
        Expand area from a given position.

        From a postion add and subtract by certain parameters.

        parameters:
            parameters: dict. User parameters.

        return:
            void
        """
        pass
