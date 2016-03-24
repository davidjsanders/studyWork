# Import base library modules - From Bluetooth symbolic link to /base_lib
from Location_Service_Config_Control.v3_00_Config_Hotspot_Control \
    import v3_00_Config_Hotspot_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Hotspot_Control(v3_00_Config_Hotspot_Control):
    def __init__(self):
        super(Config_Hotspot_Control, self).__init__()

config_hotspot_control = Config_Hotspot_Control()

