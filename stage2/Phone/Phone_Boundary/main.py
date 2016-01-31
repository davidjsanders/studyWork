from Phone import app, api
from Phone_Boundary.Location_Boundary import Location_Boundary
from Phone_Boundary.Notification_Boundary import Notification_Boundary

api.add_resource(Location_Boundary, '/v1_00/location')
api.add_resource(Notification_Boundary, '/v1_00/notification')
