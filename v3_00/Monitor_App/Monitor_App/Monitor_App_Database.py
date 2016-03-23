# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App.v3_00_Monitor_App_Database import v3_00_Monitor_App_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Monitor_App_Database(v3_00_Monitor_App_Database):
    def __init__(self, controller=None,
                       port_number='5000',
                       server_name='localhsot'):
        super(Monitor_App_Database, self).__init__(
                       controller,
                       port_number,
                       server_name)


