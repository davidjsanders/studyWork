from Module import app, api
from Module.Control import global_controller
from Module_Config_Boundary.Sample_Config_Boundary \
    import Config_Sample_Boundary
#
# Get the version of the API
#
version = global_controller.get_value('version')

api.add_resource(Config_Sample_Boundary,
                 '/{0}/config/sample'.format(version))

