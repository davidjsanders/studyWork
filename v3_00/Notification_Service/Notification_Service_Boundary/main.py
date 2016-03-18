from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service import app, api
from Notification_Service.Control import global_control
from Notification_Service_Boundary.Notification_Receive_Boundary \
    import Notification_Receive_Boundary
from Notification_Service_Boundary.Notification_Push_Boundary \
    import Notification_Push_Boundary

#
# Get the version of the API
#
version = global_control.get_value('version')

api.add_resource(Notification_Receive_Boundary,
                 '/{0}/notification'.format(version))
api.add_resource(Notification_Push_Boundary,
                 '/{0}/push'.format(version))
