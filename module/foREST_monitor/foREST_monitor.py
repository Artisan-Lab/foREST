""" Global monitor for the fuzzing run """
import json
from log.get_logging import foREST_log
from module.foREST_monitor.time_monitor import TimeMonitor
from foREST_setting import foRESTSettings


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
        self._resource_pool = None
        self._api_list = None
        self._annotation_table = None
        self._annotation_key_table = None
        foRESTMonitor.__instance = self

    @property
    def resource_pool(self):
        return self._resource_pool

    @resource_pool.setter
    def resource_pool(self, value):
        self._resource_pool = value

    def create_time_monitor(self, time_in_hour):
        """ create a time monitor.

        @param time_in_hour: Time budget in minutes.
        @type  time_in_hour: Int

        @return: None
        @rtype : None
        """
        if self._time_monitor:
            raise Exception("Attempting to create a new time monitor")
        self._time_monitor = TimeMonitor(time_in_hour)

    def start_time_monitor(self):
        """ start time monitor

        @return: None
        @rtype : None

        """
        if not self._time_monitor:
            raise Exception("time monitor uninitialized")
        self._time_monitor.setDaemon(True)
        self._time_monitor.start()

    def terminate_fuzzing(self):
        """ Terminates the fuzzing thread by stop time monitor

        @return: None
        @rtype : None

        """
        self._time_monitor.terminate()

    @property
    def time_monitor(self) -> TimeMonitor:
        return self._time_monitor

    @property
    def api_list(self):
        return self._api_list

    @api_list.setter
    def api_list(self, value):
        self._api_list = value

    @property
    def annotation_table(self):
        return self._annotation_table

    @property
    def annotation_key_table(self):
        return self._annotation_key_table

    def parsing_api_list(self, path):
        self._api_list.parsing_api_file(path)

    def parsing_external_table(self):
        if foRESTSettings().annotation_table:
            foREST_log.print("testing with annotation table")
            with open(foRESTSettings().annotation_table_file_path, 'r') as json_file:
                self._annotation_table = json.load(json_file)
        else:
            foREST_log.print("testing without annotation table")
        if foRESTSettings().annotation_table:
            foREST_log.print("testing with annotation key table")
            with open(foRESTSettings().external_key_file_path, 'r') as json_file:
                self._annotation_key_table = json.load(json_file)
        else:
            foREST_log.print("testing without annotation key table")


def Monitor() -> foRESTMonitor:
    """ Accessor for the FuzzingMonitor singleton """
    return foRESTMonitor.Instance()



