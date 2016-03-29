# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone_Config_Control.v3_00_Config_Pair_Control \
    import v3_00_Config_Pair_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Pair_Control(v3_00_Config_Pair_Control):
    def __init__(self):
        super(Config_Pair_Control, self).__init__()


pair_control_object = Config_Pair_Control()

