# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone.v3_00_Notification_Control import v3_00_Notification_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Control(v3_00_Notification_Control):
    def __init__(self):
        super(Notification_Control, self).__init__()


notification_control_object = Notification_Control()

