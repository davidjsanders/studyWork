# Import base library modules - From Bluetooth symbolic link to /base_lib
from base_lib.v1_00_Config_Logger \
    import v1_00_Config_Logger

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Logger(v1_00_Config_Logger):
    def __init__(self):
        super(Config_Logger, self).__init__()


