from Context import app, api
from Context.Control import global_controller
from Context_Config_Boundary.Config_Sample_Boundary \
    import Config_Sample_Boundary
#
# Get the version of the API
#
version = global_controller.get_value('version')

api.add_resource(Config_Sample_Boundary,
                 '/{0}/config/sample'.format(version))

