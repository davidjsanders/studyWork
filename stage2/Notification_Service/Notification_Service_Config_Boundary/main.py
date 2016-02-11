from Notification_Service import app, api
from Notification_Service_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary

api.add_resource(Config_Logger_Boundary, '/v1_00/config/logger')

