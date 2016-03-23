# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone_Config_Control.v3_00_Config_Lock_Control \
    import v3_00_Config_Lock_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Lock_Control(v3_00_Config_Lock_Control):
    def __init__(self):
        super(Config_Lock_Control, self).__init__()

lock_control_object = Config_Lock_Control()


