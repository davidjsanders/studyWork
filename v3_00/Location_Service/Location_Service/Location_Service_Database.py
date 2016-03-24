# Import base library modules - From Bluetooth symbolic link to /base_lib
from Location_Service.v3_00_Location_Service_Database \
    import v3_00_Location_Service_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Location_Service_Database(v3_00_Location_Service_Database):
    def __init__(self, server_name=None, port_number=None):
        super(Location_Service_Database, self)\
            .__init__(server_name, port_number)

