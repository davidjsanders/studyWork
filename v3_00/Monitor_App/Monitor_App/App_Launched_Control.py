# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App.v3_00_App_Launched_Control import v3_00_App_Launched_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class App_Launched_Control(v3_00_App_Launched_Control):
    def __init__(self):
        super(App_Launched_Control, self).__init__()


global_app_launched_control = App_Launched_Control()
