# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone.v4_00_Control import v4_00_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(v4_00_Control):
    def __init__(self):
        super(Control, self).__init__()


global_controller = Control()
