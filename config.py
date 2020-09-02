import configparser
import sys


class Config:
    @staticmethod
    def ReadConfig():
        if not hasattr(Config, "read_flag"):
            Config.conf = configparser.ConfigParser()
            Config.conf.read("conf.ini")
            Config.host = Config.conf.get("database", "host")
            Config.user = Config.conf.get("database", "user")
            Config.password = Config.conf.get("database", "password")
            Config.database = Config.conf.get("database", "database")
            Config.charset = "utf8"
            Config.AllFundNameTableUpdateInternal = int(Config.conf.get("update", "ALlFundName"))
            Config.read_flag = True
