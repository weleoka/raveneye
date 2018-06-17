"""
# Copyright (c) 2018 Kai Weeks.
# See LICENSE for details.

Module with class to wrap trackers under.

"""

import ravencore.main.config as raven_conf
from ravencore.utils.exceptions import *
import ravencore.utils.logging

from raveneye.trackers.dolink import Dolink

class Tracker:
    """
    Class wrapping a position tracker.

    This class can filter and verify data before passing on.
    """

    def __init__(self, tracker_list, prefered_tracker_id = None):
        """
        Constructor for class.

        parameters:
            tracker_list: dict. The users trackers.
            prefered_tracker_id: string. The prefered tracker can be set manually.

        return:
            void
        """
        name = '.'.join([__name__, self.__class__.__name__])
        self.logger = ravencore.utils.logging.getLogger(name)

        self.prefered_tracker_id = prefered_tracker_id
        self.tracker_list = tracker_list
        self.selected_tracker = self.select_tracker(prefered_tracker_id)

        self.debug = self.selected_tracker['debug']

        self.tracker_type = None # The tracker type once identified.
        self.tracker = None # The instance of the tracker.

        self.new_tracker()


    def new_tracker(self):
        """
        Identify tracker type from a list of valid trackers.

        Once identified the relevant class can be instanciated.

        parameters:

        return:
            void
        """
        # Check if users tracker is supported. This is a redundant check.
        if self.selected_tracker['type'] in raven_conf.supported_trackers:
            self.tracker_type = self.selected_tracker['type']

            # Identify and instansiate the service with user parameters.
            if self.tracker_type == 'dolink':
                self.tracker = Dolink(self.selected_tracker)

        else:

            raise RavenException("No such supported tracker: %s" % (self.selected_tracker['type']))


    def select_tracker(self, tracker_id):
        """
        Select one tracker from list.

        From a list of multiple trackers, use only one.

        parameters:
            tracker_id: string. The prefered tracker.

        return:
            void
        """

        if not tracker_id:

            raise RavenException("Currently have to manually choose preferred tracker")

        try:

            return self.tracker_list.get(tracker_id) # Get the trackers data.

        except KeyError:

            raise RavenException("Tracker %s not found in users list of trackers." % (tracker_id))


    def get_position(self):
        """
        Get the position data from tracker.

        The data can be in different formats.

        #-> Need to screen incoming data in general.

        parameters:

        return:
            void
        """
        self.tracker.get_position()

        # Add the tracker details to position data.
        self.tracker.position['position_source'] = (self.tracker_type, self.prefered_tracker_id)

        self.position = self.tracker.position



        return True
