#!/usr/bin/python3
from v3_00_Show_Log import v3_00_Show_Log

#
# SuperClass.
# ----------------------------------------------------------------------------
class Show_Log(v3_00_Show_Log):
    def __init__(self):
        super(Show_Log, self).__init__()


global_Show_Log = Show_Log()

