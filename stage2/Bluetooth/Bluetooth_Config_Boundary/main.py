from Bluetooth import app, api
from Bluetooth_Config_Boundary.Config_Output_Boundary \
    import Config_Output_Boundary
from Bluetooth_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary

api.add_resource(Config_Logger_Boundary, '/v1_00/config/logger')
api.add_resource(Config_Output_Boundary,
                 '/v1_00/config/output/<string:devicename>')

