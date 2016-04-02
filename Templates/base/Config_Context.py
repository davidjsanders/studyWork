# Import base library modules - From Bluetooth symbolic link to /base_lib
from base_lib.v1_00_Config_Context \
    import v1_00_Config_Context

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Context(v1_00_Config_Context):
    def __init__(self, control=None, module=None):
        super(Config_Context, self).__init__(control, module)

