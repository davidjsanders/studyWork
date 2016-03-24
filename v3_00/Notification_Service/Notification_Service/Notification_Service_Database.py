# Import base library modules - From Bluetooth symbolic link to /base_lib
from Notification_Service.v3_00_Notification_Service_Database \
    import v3_00_Notification_Service_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Service_Database(v3_00_Notification_Service_Database):
    def __init__(self,
                 port_number='5000',
                 server_name='localhost'):
        super(Notification_Service_Database, self)\
           .__init__(port_number,
                     server_name)


