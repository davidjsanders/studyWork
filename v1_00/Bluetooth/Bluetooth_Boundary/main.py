from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api
from Bluetooth.Control import global_control
from Bluetooth_Boundary import apiR
from Bluetooth_Boundary.Pair_Boundary import Pair_Boundary
from Bluetooth_Boundary.Broadcast_Boundary import Broadcast_Boundary

#
# Get the version of the API
#
version = global_control.get_value('version')

apiR.add_resource(Broadcast_Boundary,
                  '/{0}/broadcast/<string:devicename>'.format(version))
apiR.add_resource(Pair_Boundary,
                  '/{0}/pair/<string:devicename>'.format(version))

