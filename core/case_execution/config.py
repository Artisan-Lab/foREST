from configparser import ConfigParser
import os
import redis


class TestingConfig:
    """
    load parameters from config file or redis
    """

    def __init__(self):
        """
        start loading
        """
        config = ConfigParser()
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../restfultest_config.ini")
        config.read(path, encoding='UTF-8')
        self.db_params = int(config.get('redis', 'db_params'))
        self.db_success = int(config.get('redis', 'db_success'))
        self.db_parallelism = int(config.get('redis', 'db_parallelism'))
        self.db_fuzz_pool = int(config.get('redis', 'db_fuzz_pool'))
        self.db_serial = int(config.get('redis', 'db_serial'))
        self.db_o = int(config.get('redis', 'db_o'))
        self.redis_host = config.get('redis', 'host')
        self.redis_port = config.get('redis', 'port')
        self.params_pool = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.db_params,
                                             decode_responses=True)
        self.success_pool = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.db_success,
                                              decode_responses=True)
        self.fuzz_pool = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.db_fuzz_pool,
                                           decode_responses=True)
        self.flag = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.db_o, decode_responses=True)
