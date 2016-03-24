from base_lib.Config_Logger import Config_Logger
from Bluetooth import Control

class v3_00_Config_Logger_Control(object):
    controller = None
    config_logger = None

    def __init__(self):
        self.controller = Control.global_control
        self.config_logger = Config_Logger(self.controller)

    def get_logger(self):
        return self.config_logger.get_logger()

    def remove_logger(self, json_string=None):
        return self.config_logger.remove_logger(json_string)

    def set_logger(self, json_string=None):
        return self.config_logger.set_logger(json_string)

