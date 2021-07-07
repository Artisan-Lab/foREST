# import the Redis client
import time  # 引入time模块

import redis
from log.get_logging import Log
coverage_log = Log(log_name='restler_coverage.log')

class RedisCoverage:
    """
    coverage from redis
    """

    def __init__(self):
        # Create a redis client

        self.redis_client = redis.StrictRedis(host='10.177.75.243', charset="utf-8", decode_responses=True, db='db1')
        self.SUM_FILES = '0'
        self.SUM_LINES = '0'
        self.SUM_EXCUTABLE = '0'
        self.SUM_COVERED = '0'
        self.SUM_COVERRATE = '0%'

    def get_coverage(self):
        """
        get_coverage
        """
        self.php_coverage_data = self.redis_client.hgetall('php_coverage_data')  # type dict
        if self.php_coverage_data is not None and len(self.php_coverage_data) > 0:
            self.SUM_FILES = self.php_coverage_data['SUM_FILES']
            self.SUM_LINES = self.php_coverage_data['SUM_LINES']
            self.SUM_EXCUTABLE = self.php_coverage_data['SUM_EXCUTABLE']
            self.SUM_COVERED = self.php_coverage_data['SUM_COVERED']
            self.SUM_COVERRATE = self.php_coverage_data['SUM_COVERRATE']

    def write_time_and_coverage_to_file(self):
        """
        write time and coverage
        """
        f = open("restler_coverage.log", "a")
        self.get_coverage()
        f.write(str(time.time()) + " " + str(self.SUM_COVERED) + " " + str(self.SUM_COVERRATE) + "\n");
        f.close()


if __name__ == '__main__':
    while True:
        RedisCoverage().write_time_and_coverage_to_file()
        time.sleep(0.05)
