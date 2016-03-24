# Import base library modules - From Bluetooth symbolic link to /base_lib
from Logger.v3_00_Log_Control \
    import v3_00_Log_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class Log_Control(v3_00_Log_Control):
    def __init__(self):
        super(Log_Control, self).__init__()

global_log_control = Log_Control()
