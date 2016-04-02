# Import base library modules - From Bluetooth symbolic link to /base_lib
from Context_Config_Control.v4_00_Config_Context_Control \
    import v4_00_Config_Context_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Context_Control(v4_00_Config_Context_Control):
    def __init__(self):
        super(Config_Context_Control, self).__init__()

context_control_object = Config_Context_Control()

