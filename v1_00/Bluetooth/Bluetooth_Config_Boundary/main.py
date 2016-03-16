from Bluetooth import app, api
from Bluetooth.Control import global_control
from Bluetooth_Config_Boundary.Config_Output_Boundary \
    import Config_Output_Boundary
from Bluetooth_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary

#
# Get the version of the API
#
version = global_control.get_value('version')

api.add_resource(Config_Logger_Boundary,
                 '/{0}/config/logger'.format(version))
api.add_resource(Config_Output_Boundary,
                 '/{0}/config/output/<string:devicename>'.format(version))

