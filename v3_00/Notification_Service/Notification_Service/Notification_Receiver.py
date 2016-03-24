# Import base library modules - From Bluetooth symbolic link to /base_lib
from Notification_Service.v3_00_Notification_Receiver \
    import v3_00_Notification_Receiver

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Receiver(v3_00_Notification_Receiver):
    def __init__(self):
        super(Notification_Receiver, self).__init__()


global_notification_receiver_control = Notification_Receiver()
