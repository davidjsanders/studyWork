# Import base library modules - From Bluetooth symbolic link to /base_lib
from Notification_Service.v3_00_Notification_Processor \
    import v3_00_Notification_Processor

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Processor(v3_00_Notification_Processor):
    def __init__(self):
        super(Notification_Processor, self).__init__()

