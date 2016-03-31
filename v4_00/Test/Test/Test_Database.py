# Import base library modules - From Bluetooth symbolic link to /base_lib
from Test.v1_00_Test_Database import v1_00_Test_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class Test_Database(v1_00_Test_Database):
    def __init__(self,
                 controller=None,
                 server_name='localhost',
                 port_number=5000):
        super(Test_Database, self).__init__(controller,
                                             server_name,
                                             port_number)

