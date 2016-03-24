# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App.v3_01_Location_Processor import v3_01_Location_Processor

#
# SuperClass.
# ----------------------------------------------------------------------------
class Location_Processor(v3_01_Location_Processor):
    def __init__(self):
        super(Location_Processor, self).__init__()

