import os
import configparser


class ReadConfig:

    @staticmethod
    def readconfig(title, key):
        conf = configparser.ConfigParser()
        root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../FoREST_config.conf")
        conf.read(root_path)
        return conf.get(title, key)