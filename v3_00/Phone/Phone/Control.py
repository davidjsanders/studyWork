# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone.v3_00_Control import v3_00_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(v3_00_Control):
    def __init__(self):
        super(Control, self).__init__()


global_controller = Control()
