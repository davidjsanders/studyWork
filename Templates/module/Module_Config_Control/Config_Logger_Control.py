# Import base library modules - From Bluetooth symbolic link to /base_lib
from Module_Config_Control.v1_00_Config_Logger_Control \
    import v1_00_Config_Logger_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Logger_Control(v1_00_Config_Logger_Control):
    def __init__(self):
        super(Config_Logger_Control, self).__init__()

logger_control_object = Config_Logger_Control()

