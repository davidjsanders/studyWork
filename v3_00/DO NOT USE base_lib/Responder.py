from flask import Response
import json

class Responder(object):

    def do(self,
          status=200,
          response='success',
          data=None,
          message=''
    ):
        return_dict = {"status":status,
                       "response":response,
                       "data":data,
                       "message":message}

        return Response(
            json.dumps(return_dict),
            status=status,
            mimetype='application/json')

