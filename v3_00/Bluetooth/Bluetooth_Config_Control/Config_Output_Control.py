# Import base library modules - From Bluetooth symbolic link to /base_lib
from Bluetooth_Config_Control.v3_00_Config_Output_Control \
    import v3_00_Config_Output_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Output_Control(v3_00_Config_Output_Control):
    def __init__(self):
        super(Config_Output_Control, self).__init__()

config_output_control_object = Config_Output_Control()
