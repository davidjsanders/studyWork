# Import base library modules - From Bluetooth symbolic link to /base_lib
from Context.v3_00_Context_Database import v3_00_Context_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Context_Database(v3_00_Context_Database):
    def __init__(self,
                 controller=None,
                 server_name='localhost',
                 port_number=5000):
        super(Context_Database, self).__init__(controller,
                                             server_name,
                                             port_number)

