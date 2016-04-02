# Import base library modules - From Bluetooth symbolic link to /base_lib
from Context_Config_Control.v4_00_Config_Preferences_Control \
    import v4_00_Config_Preferences_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Preferences_Control(v4_00_Config_Preferences_Control):
    def __init__(self):
        super(Config_Preferences_Control, self).__init__()


config_preferences_control_object = Config_Preferences_Control()

