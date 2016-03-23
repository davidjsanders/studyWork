# Import base library modules - From Bluetooth symbolic link to /base_lib
from Phone.v3_00_Phone_Database import v3_00_Phone_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Phone_Database(v3_00_Phone_Database):
    def __init__(self,
                 controller=None,
                 server_name='localhost',
                 port_number=5000):
        super(Phone_Database, self).__init__(controller,
                                             server_name,
                                             port_number)

