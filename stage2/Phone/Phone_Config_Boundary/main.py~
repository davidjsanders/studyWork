from Phone import app, api
from Phone_Config_Boundary.Config_Lock_Boundary import Config_Lock_Boundary
from Phone_Config_Boundary.Config_Unlock_Boundary import Config_Unlock_Boundary
from Phone_Config_Boundary.Config_Pair_Boundary import Config_Pair_Boundary
from Phone_Config_Boundary.Config_Monitor_App_Boundary \
    import Config_Monitor_App_Boundary
from Phone_Config_Boundary.Config_Push_Notifications_Boundary \
    import Config_Push_Notifications_Boundary
from Phone_Config_Boundary.Config_Launch_Boundary import Config_Launch_Boundary

api.add_resource(Config_Monitor_App_Boundary, '/v1_00/config/monitor')
api.add_resource(Config_Lock_Boundary, '/v1_00/config/lock')
api.add_resource(Config_Unlock_Boundary, '/v1_00/config/unlock')
api.add_resource(Config_Pair_Boundary, '/v1_00/config/pair')
api.add_resource(Config_Launch_Boundary, '/v1_00/config/launch/<string:app>')
api.add_resource(Config_Push_Notifications_Boundary,
                 '/v1_00/config/push')

