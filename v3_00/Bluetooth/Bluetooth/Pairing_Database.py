# Import base library modules - From Bluetooth symbolic link to /base_lib
from Bluetooth.v3_00_Pairing_Database import v3_00_Pairing_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Pairing_Database(v3_00_Pairing_Database):
    def __init__(self, server_name=None, port_number=None):
        super(Pairing_Database, self)\
            .__init__(server_name, port_number)

