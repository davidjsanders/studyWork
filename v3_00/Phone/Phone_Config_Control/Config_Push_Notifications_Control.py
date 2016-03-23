# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone_Config_Control.v3_00_Config_Push_Notifications_Control \
    import v3_00_Config_Push_Notifications_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Push_Notifications_Control(v3_00_Config_Push_Notifications_Control):
    def __init__(self):
        super(Config_Push_Notifications_Control, self).__init__()


push_control_object = Config_Push_Notifications_Control()


