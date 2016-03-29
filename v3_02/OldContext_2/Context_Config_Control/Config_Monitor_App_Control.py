# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone_Config_Control.v3_00_Config_Monitor_App_Control \
    import v3_00_Config_Monitor_App_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Monitor_App_Control(v3_00_Config_Monitor_App_Control):
    def __init__(self):
        super(Config_Monitor_App_Control, self).__init__()


monitor_app_control_object = Config_Monitor_App_Control()

