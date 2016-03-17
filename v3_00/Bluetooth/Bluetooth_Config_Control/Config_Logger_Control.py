from base_lib.Config_Logger import Config_Logger
from Bluetooth import Control

class Config_Logger_Control(object):
    __controller = None
    __config_logger = None

    def __init__(self):
        self.__controller = Control.global_control
        self.__config_logger = Config_Logger(self.__controller)

    def get_logger(self):
        return self.__config_logger.get_logger()

    def remove_logger(self, json_string=None):
        return self.__config_logger.remove_logger(json_string)

    def set_logger(self, json_string=None):
        return self.__config_logger.set_logger(json_string)

logger_control_object = Config_Logger_Control()

