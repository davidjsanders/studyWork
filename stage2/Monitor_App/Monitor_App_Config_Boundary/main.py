from Monitor_App import app, api
from Monitor_App_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary

api.add_resource(Config_Logger_Boundary, '/v1_00/config/logger')

