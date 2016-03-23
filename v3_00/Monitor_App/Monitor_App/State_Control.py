# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App.v3_00_State_Control import v3_00_State_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class State_Control(v3_00_State_Control):
    def __init__(self):
        super(State_Control, self).__init__()

global_state_control = State_Control()
