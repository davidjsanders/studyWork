# Import base library modules - From Bluetooth symbolic link to /base_lib
from Location_Service.v3_00_Check_Control \
    import v3_00_Check_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Check_Control(v3_00_Check_Control):
    def __init__(self):
        super(Check_Control, self).__init__()

global_check_control = Check_Control()
