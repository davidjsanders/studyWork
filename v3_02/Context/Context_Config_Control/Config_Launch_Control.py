# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone_Config_Control.v3_00_Config_Launch_Control \
    import v3_00_Config_Launch_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Launch_Control(v3_00_Config_Launch_Control):
    def __init__(self):
        super(Config_Launch_Control, self).__init__()


launch_control_object = Config_Launch_Control()

