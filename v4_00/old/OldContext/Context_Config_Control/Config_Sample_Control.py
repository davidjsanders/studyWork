# Import base library contexts - From Bluetooth symbolic link to /base_lib
from Context_Config_Control.v1_00_Config_Sample_Control \
    import v1_00_Config_Sample_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Sample_Control(v1_00_Config_Sample_Control):
    def __init__(self):
        super(Config_Sample_Control, self).__init__()


config_sample_control_object = Config_Sample_Control()

