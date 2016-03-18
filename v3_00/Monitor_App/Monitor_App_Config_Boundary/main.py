from Monitor_App import app, api
from Monitor_App.Control import global_control
from Monitor_App_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary

#
# Get the version of the API
#
version = global_control.get_value('version')

api.add_resource(Config_Logger_Boundary, '/{0}/config/logger'.format(version))

