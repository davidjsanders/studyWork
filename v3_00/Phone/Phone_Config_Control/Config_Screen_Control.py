# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone_Config_Control.v3_00_Config_Screen_Control import v3_00_Config_Screen_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Screen_Control(v3_00_Config_Screen_Control):
    def __init__(self):
        super(Config_Screen_Control, self).__init__()


screen_control_object = Config_Screen_Control()


