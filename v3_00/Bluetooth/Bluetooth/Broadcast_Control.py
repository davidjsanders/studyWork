# Import base library modules - From Bluetooth symbolic link to /base_lib
from Bluetooth.v3_00_Broadcast_Control import v3_00_Broadcast_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Broadcast_Control(v3_00_Broadcast_Control):
    def __init__(self):
        super(Broadcast_Control, self).__init__()

global_broadcast_control = Broadcast_Control()
