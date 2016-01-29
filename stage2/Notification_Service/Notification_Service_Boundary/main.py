from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service import app, api
from Notification_Service_Boundary import apiR
from Notification_Service_Boundary.Location_Boundary import Location_Boundary
from Notification_Service_Boundary.Notification_Receive_Boundary \
    import Notification_Receive_Boundary

apiR.add_resource(Location_Boundary, '/v1_00/location')
apiR.add_resource(Notification_Receive_Boundary, '/v1_00/notification')
