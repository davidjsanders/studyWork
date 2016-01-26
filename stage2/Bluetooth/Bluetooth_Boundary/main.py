from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api
from Bluetooth_Boundary import apiR
from Bluetooth_Boundary.Pair_Boundary import Pair_Boundary
from Bluetooth_Boundary.Broadcast_Boundary import Broadcast_Boundary

apiR.add_resource(Broadcast_Boundary, '/v1_00/broadcast/<string:devicename>')
apiR.add_resource(Pair_Boundary, '/v1_00/pair/<string:devicename>')
