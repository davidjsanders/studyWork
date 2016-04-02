from Context import app, api
from Context.Control import global_controller
from Context_Config_Boundary.Config_Sample_Boundary \
    import Config_Sample_Boundary
from Context_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary
from Context_Config_Boundary.Config_Context_Boundary \
    import Config_Context_Boundary
#
# Get the version of the API
#
version = global_controller.get_value('version')

api.add_resource(Config_Sample_Boundary,
                 '/{0}/config/sample'.format(version))
#
# Place config boundaries here
#
# End config boundaries here
#
api.add_resource(Config_Logger_Boundary,
                 '/{0}/config/logger'.format(version))
api.add_resource(Config_Context_Boundary,
                 '/{0}/config/context'.format(version))

### Generated path for service: Preferences
from Context_Config_Boundary.Preferences_Boundary import Config_Preferences_Boundary
api.add_resource(Config_Preferences_Boundary, '/{0}/config/preferences'.format(version))
