# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App.v3_01_Control import v3_01_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(v3_01_Control):
    def __init__(self):
        super(Control, self).__init__()


global_control = Control()
