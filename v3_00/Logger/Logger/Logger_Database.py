# Import base library modules - From Bluetooth symbolic link to /base_lib
from Logger.v3_00_Logger_Database \
    import v3_00_Logger_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Logger_Database(v3_00_Logger_Database):
    def __init__(self, server_name=None, port_number=None):
        super(Logger_Database, self)\
            .__init__(server_name, port_number)



