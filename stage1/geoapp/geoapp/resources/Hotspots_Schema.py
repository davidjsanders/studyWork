from flask_restful import Resource
from geoapp import app, api

from geoapp.resources.Response import Response_Object
import geoapp.resources.Config as Config

class Hotspots_Schema(Resource):
    def get(self):
        schema = {
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "id": 'http://'+Config.server_name+':'+ \
                          str(Config.port_number)+\
                          api.url_for(Hotspots_Schema,
                                      _external=Config.ext_mode),
                    "type": "object",
                    "properties": {
                        "hotspot":
                        {
                            "type": "string",
                            "description":"The hotspot name",
                            "default":"new note"
                        },
                        "start-x":
                        {
                            "type": "number",
                            "description":"The start X co-ordinate",
                            "default":0
                        },
                        "start-y":
                        {
                            "type": "number",
                            "description":"The start Y co-ordinate",
                            "default":0
                        },
                        "end-x":
                        {
                            "type": "number",
                            "description":"The end X co-ordinate",
                            "default":0
                        },
                        "end-y":
                        {
                            "type": "number",
                            "description":"The end Y co-ordinate",
                            "default":0
                        }
                    },
                 "required": ["start-x", "start-y", "end-x", "end-y"]
                 }
        return_list = []
        return_status = 200
        return_success_fail = 'success'
        return_message = 'notification schema'
        try:
            return_list = schema
        except Exception as e:
            return_status = 400
            return_success_fail = 'error'
            return_message = repr(e)

        return Response_Object(
                data=return_list,
                status=return_status,
                success_fail=return_success_fail,
                message=return_message
            ).response()

