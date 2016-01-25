from flask_restful import Resource, Api, reqparse, abort
from flask import Response
#from Bluetooth import app
from BluetoothReceiver import apiR
from BluetoothReceiver.PairBoundary import PairBoundary
from BluetoothReceiver.BroadcastBoundary import BroadcastBoundary

apiR.add_resource(BroadcastBoundary, '/broadcast/<string:devicename>')
apiR.add_resource(PairBoundary, '/pair/<string:devicename>')
