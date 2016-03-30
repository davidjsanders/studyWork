# Import base library contexts - From Bluetooth symbolic link to /base_lib
from Context.v1_00_Control import v1_00_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(v1_00_Control):
    def __init__(self):
        super(Control, self).__init__()


global_controller = Control()
