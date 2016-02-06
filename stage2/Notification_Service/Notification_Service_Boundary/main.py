from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service import app, api
from Notification_Service_Boundary.Notification_Receive_Boundary \
    import Notification_Receive_Boundary
from Notification_Service_Boundary.Notification_Push_Boundary \
    import Notification_Push_Boundary

api.add_resource(Notification_Receive_Boundary, '/v1_00/notification')
api.add_resource(Notification_Push_Boundary, '/v1_00/push')
