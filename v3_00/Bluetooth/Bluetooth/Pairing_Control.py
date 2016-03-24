# Import base library modules - From Bluetooth symbolic link to /base_lib
from Bluetooth.v3_00_Pairing_Control import v3_00_Pairing_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Pairing_Control(v3_00_Pairing_Control):
    def __init__(self):
        super(Pairing_Control, self).__init__()

global_pair_control = Pairing_Control()
