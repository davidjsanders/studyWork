from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api
from BluetoothBoundary import apiR
from BluetoothBoundary.PairBoundary import PairBoundary
from BluetoothBoundary.BroadcastBoundary import BroadcastBoundary

apiR.add_resource(BroadcastBoundary, '/v1_00/broadcast/<string:devicename>')
apiR.add_resource(PairBoundary, '/v1_00/pair/<string:devicename>')
