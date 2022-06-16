""" Global monitor for the fuzzing run """
import time
from module.foREST_monitor.clock_monitor import TimeThread


def Monitor():
    """ Accessor for the FuzzingMonitor singleton """
    return foRESTMonitor.Instance()


class foRESTMonitor(object):
    __instance = None

    @staticmethod
    def Instance():
        """ Singleton's instance accessor

        @return FuzzingMonitor instance
        @rtype  FuzzingMonitor

        """
        if foRESTMonitor.__instance is None:
            raise Exception("foREST Monitor not yet initialized.")
        return foRESTMonitor.__instance

    def __init__(self):
        if foRESTMonitor.__instance:
            raise Exception("Attempting to create a new singleton instance.")

        self._time_monitor = None
        foRESTMonitor.__instance = self

    def create_time_monitor(self, time_in_minutes):
        """ create a time monitor.

        @param time_in_minutes: Time budget in minutes.
        @type  time_in_minutes: Int

        @return: None
        @rtype : None
        """
        if self._time_monitor:
            raise Exception("Attempting to create a new time monitor")
        self._time_monitor = TimeThread(time_in_minutes)

    def start_time_monitor(self):
        """ start time monitor

        @return: None
        @rtype : None

        """
        if not self._time_monitor:
            raise Exception("time monitor uninitialized")
        self._time_monitor.start()

    def terminate_fuzzing(self):
        """ Terminates the fuzzing thread by stop time monitor

        @return: None
        @rtype : None

        """
        self._time_monitor.terminate()



