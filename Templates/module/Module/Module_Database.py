# Import base library modules - From Bluetooth symbolic link to /base_lib
from Module.v1_00_Module_Database import v1_00_Module_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Module_Database(v1_00_Module_Database):
    def __init__(self,
                 controller=None,
                 server_name='localhost',
                 port_number=5000):
        super(Module_Database, self).__init__(controller,
                                             server_name,
                                             port_number)

