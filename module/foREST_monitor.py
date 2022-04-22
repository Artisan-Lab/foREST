""" Global monitor for the fuzzing run """
import time


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

        # timestamp of the beginning of fuzzing session
        self._start_time = int(time.time()*10**6)

        # time budget to stop fuzzing jobs (time in hours)
        self._time_budget = 24*30 # (~ 1 month)

        foRESTMonitor.__instance = self


    def set_time_budget(self, time_in_hours):
        """ Set the initial time budget.

        @param time_in_hours: Time budget in hours.
        @type  time_in_hours: Int

        @return: None
        @rtype : None

        """
        self._time_budget = 10**6*3600*float(time_in_hours)

    def reset_start_time(self):
        """ Resets start time to now (time of routine's invocation in
            microseconds).

        @return: None
        @rtype : None

        """
        self._start_time = int(time.time()*10**6)


    @property
    def running_time(self):
        """ Returns the running time.

        @return: Running time in microseconds.
        @rtype : int

        """
        _running_time = int(time.time()*10**6) - self._start_time
        return _running_time

    @property
    def remaining_time_budget(self):
        """ Returns the time remaining from the initial budget.

        @return: Remaining time in microseconds.
        @rtype : int

        """
        running_time = int(time.time()*10**6) - self._start_time
        return self._time_budget - running_time

    @property
    def start_time(self):
        """ Returns start time of fuzzing.

        @return: The start time in seconds.
        @rtype : int

        """
        return self._start_time

    def terminate_fuzzing(self):
        """ Terminates the fuzzing thread by setting the time budget to zero

        @return: None
        @rtype : None

        """
        self._time_budget = 0.0



