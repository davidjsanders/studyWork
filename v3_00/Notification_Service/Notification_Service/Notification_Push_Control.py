# Import base library modules - From Bluetooth symbolic link to /base_lib
from Notification_Service.v3_00_Notification_Push_Control \
    import v3_00_Notification_Push_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Push_Control(v3_00_Notification_Push_Control):
    def __init__(self):
        super(Notification_Push_Control, self).__init__()

global_notification_push_control = Notification_Push_Control()
