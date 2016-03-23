# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone_Config_Control.v3_00_Config_Location_Control \
    import v3_00_Config_Location_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Location_Control(v3_00_Config_Location_Control):
    def __init__(self):
        super(Config_Location_Control, self).__init__()


config_location_control_object = Config_Location_Control()

