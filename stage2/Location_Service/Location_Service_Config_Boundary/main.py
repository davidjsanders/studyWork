from Location_Service import app, api
from Location_Service.Control import global_control
from Location_Service_Config_Boundary.Config_Hotspot_Boundary \
    import Config_Hotspot_Boundary, Config_Hotspot_All_Boundary
from Location_Service_Config_Boundary.Config_Logger_Boundary \
    import Config_Logger_Boundary

#
# Get the version of the API
#
version = global_control.get_value('version')

api.add_resource(Config_Hotspot_Boundary,
                 '/{0}/config/hotspot/<string:location>'.format(version))
api.add_resource(Config_Hotspot_All_Boundary,
                 '/{0}/config/hotspots'.format(version))
api.add_resource(Config_Logger_Boundary,
                 '/{0}/config/logger'.format(version))

