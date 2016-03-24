# Import base library modules - From Bluetooth symbolic link to /base_lib
from Logger.v3_00_Logging_Processor \
    import v3_00_Logging_Processor

#
# SuperClass.
# ----------------------------------------------------------------------------
class Logging_Processor(v3_00_Logging_Processor):
    def __init__(self):
        super(Logging_Processor, self).__init__()


