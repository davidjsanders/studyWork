from base_lib.Config_Context import Config_Context
from Context import Control

class v4_00_Config_Context_Control(object):
    controller = None
    config_context = None

    def __init__(self):
        self.controller = Control.global_controller
        self.config_context = Config_Context(self.controller, module='Context')
        self.get_context_engine = self.config_context.get_context_engine
        self.set_context_engine = self.config_context.set_context_engine
        self.clear_context_engine = self.config_context.clear_context_engine

