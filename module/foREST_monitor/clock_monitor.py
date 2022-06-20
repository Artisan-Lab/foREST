import threading
import time

TESTING_MINUTES = 360


def progressbar(curr, total, duration=10, extra=''):
    """

    @param curr: spend time
    @type curr: int
    @param total: total time
    @type total: int
    @param duration: Display character length
    @type duration: int
    @param extra: extra information
    @type extra: str
    @return: None
    @rtype: None
    """
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🌲' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')


def Time_Monitor():
    """ Accessor for the FuzzingMonitor singleton """
    return TimeMonitor.Instance()

class TimeMonitor(threading.Thread):
    __instance = None
    """
        timer thread class
        Used to control testing runtime
    """

    @staticmethod
    def Instance():
        """ Singleton's instance accessor

        @return FuzzingMonitor instance
        @rtype  FuzzingMonitor

        """
        if TimeMonitor.__instance is None:
            raise Exception("time Monitor not yet initialized.")
        return TimeMonitor.__instance

    def __init__(self, total_time: int):
        """

        @param total_time: testing time in minutes
        """
        threading.Thread.__init__(self)

        if self.__instance:
            raise Exception("Attempting to create a new singleton instance.")

        self._total_time = total_time
        self._is_running = True
        self._start_time = time.perf_counter()
        self._remain_time = total_time
        self._testing_time = 0
        self.__instance = self

    def terminate(self):
        """
            Change the timer state, stop the timer
        @return: None
        """
        self._is_running = False

    @property
    def start_time(self):
        """

        @return: start time
        @rtype: time
        """
        return self._start_time

    @property
    def remain_time(self):
        """
            get remain time
        @return: remain time
        @rtype: int: seconds
        """
        return self._remain_time

    @property
    def testing_time(self):
        """
            get testing time
        @return: testing time
        @rtype: int seconds
        """
        return self._testing_time

    def run(self):
        """
            start time monitor thread
        @return: None
        @rtype: None
        """
        print(f'🌲 testing {self._total_time} minutes. Ctrl+C to exit')
        self.clock_monitor(self._total_time)

    def clock_monitor(self, minutes: int):
        """
            time monitor
        @param minutes: testing time
        @type minutes: int
        @return: None
        @rtype: None
        """
        while self._is_running:
            self._testing_time = int(round(time.perf_counter() - self._start_time))
            self._remain_time = minutes * 60 - self._testing_time
            if self._remain_time <= 0:
                print('')
                break

            countdown = '{}:{}:{} ⏰'.format(int(self._remain_time / 3600),
                                            int(self._remain_time / 60) if self._remain_time / 60 >= 10 else
                                            "0" + str(int(self._remain_time / 60)),
                                            int(self._remain_time % 60) if self._remain_time % 60 >= 10 else
                                            "0" + str(int(self._remain_time % 60)))
            duration = 25 if minutes < 25 else minutes
            progressbar(self._testing_time, minutes * 60, duration, countdown)
            time.sleep(1)


if __name__ == "__main__":
    time_thread = TimeMonitor(1)
    time_thread.start()
    try:
        while time_thread.is_alive():
            continue
    except KeyboardInterrupt:
        time_thread.terminate()
    print(1)
