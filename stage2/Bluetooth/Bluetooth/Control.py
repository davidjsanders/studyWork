from flask_restful import Resource, Api, reqparse, abort
from flask import Response

import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):

    def do_response(self,
                    status=200,
                    response='success',
                    data=None,
                    message=''):
        return_dict = {"status":status,
                       "response":response,
                       "data":data,
                       "message":message}
        return Response(
            json.dumps(return_dict),
            status=status,
            mimetype='application/json')


#
# Version 1.00
# ----------------------------------------------------------------------------
class Control_v1_00(Control):
    def future(self):
        pass

