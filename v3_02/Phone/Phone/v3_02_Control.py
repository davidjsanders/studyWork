# Import base library modules - From Bluetooth symbolic link to /base_lib
import base_lib
from base_lib.Responder import Responder
from base_lib.Config_Logger import Config_Logger
from base_lib.Logger import Logger
from base_lib.Environment import Environment
from base_lib.KVStore import KVStore

from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone.Phone_Database import Phone_Database

import datetime, time, json, os, redis, requests
from textwrap import wrap
from Phone.v3_01_Control import v3_01_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_02_Control(v3_01_Control):

    def __init__(self):
        super(v3_02_Control, self).__init__()
        print()
        print('Inside the v3_02 version :) ')
        print()

