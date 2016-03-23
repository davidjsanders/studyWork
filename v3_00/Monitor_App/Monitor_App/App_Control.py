# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App.v3_00_App_Control import v3_00_App_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class App_Control(v3_00_App_Control):
    def __init__(self):
        super(App_Control, self).__init__()

global_app_control = App_Control()
