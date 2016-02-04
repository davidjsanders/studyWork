from Location_Service import app, api
from Location_Service_Config_Boundary.Config_Hotspot_Boundary \
    import Config_Hotspot_Boundary, Config_Hotspot_All_Boundary

api.add_resource(Config_Hotspot_Boundary,
                 '/v1_00/config/hotspot/<string:location>')
api.add_resource(Config_Hotspot_All_Boundary,
                 '/v1_00/config/hotspots')

