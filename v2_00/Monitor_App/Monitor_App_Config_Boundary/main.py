from Monitor_App import app, api
from Monitor_App_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary
from Monitor_App_Config_Boundary.Config_Message_Boundary \
    import Config_Message_Boundary

api.add_resource(Config_Logger_Boundary, '/v1_00/config/logger')
api.add_resource(Config_Message_Boundary, '/v1_00/config/message/<string:msg>')

