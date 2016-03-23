# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone.v3_01_Notification_Control import v3_01_Notification_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Control(v3_01_Notification_Control):
    def __init__(self):
        super(Notification_Control, self).__init__()
        print('Notification Control Initialized.')


notification_control_object = Notification_Control()

