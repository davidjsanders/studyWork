# Import base library modules - From Bluetooth symbolic link to /base_lib
from Monitor_App_Config_Control.v3_01_Config_Message_Control \
    import v3_01_Config_Message_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Config_Message_Control(v3_01_Config_Message_Control):
    def __init__(self):
        super(Config_Message_Control, self).__init__()


logger_message_object = Config_Message_Control()

