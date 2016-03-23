# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App_Config_Control.v3_00_Config_Logger_Control \
    import v3_00_Config_Logger_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Logger_Control(v3_00_Config_Logger_Control):
    def __init__(self):
        super(Config_Logger_Control, self).__init__()


logger_control_object = Config_Logger_Control()

