from Phone import app, api
from Phone.Control import global_controller
from Phone_Config_Boundary.Config_Lock_Boundary import Config_Lock_Boundary
from Phone_Config_Boundary.Config_Unlock_Boundary import Config_Unlock_Boundary
from Phone_Config_Boundary.Config_Logger_Boundary import Config_Logger_Boundary
from Phone_Config_Boundary.Config_Pair_Boundary import Config_Pair_Boundary
from Phone_Config_Boundary.Config_Monitor_App_Boundary \
    import Config_Monitor_App_Boundary
from Phone_Config_Boundary.Config_Push_Notifications_Boundary \
    import Config_Push_Notifications_Boundary
from Phone_Config_Boundary.Config_Launch_Boundary import Config_Launch_Boundary
from Phone_Config_Boundary.Config_Location_Boundary \
    import Config_Location_Boundary
from Phone_Config_Boundary.Config_Screen_Boundary import Config_Screen_Boundary
from Phone_Config_Boundary.Config_Context_Boundary \
    import Config_Context_Boundary

#
# Get the version of the API
#
version = global_controller.get_value('version')

api.add_resource(Config_Screen_Boundary,
                 '/{0}/config/screen'.format(version))
api.add_resource(Config_Launch_Boundary,
                 '/{0}/config/launch/<string:app>'.format(version))
api.add_resource(Config_Location_Boundary,
                 '/{0}/config/location'.format(version))
api.add_resource(Config_Lock_Boundary,
                 '/{0}/config/lock'.format(version))
api.add_resource(Config_Logger_Boundary,
                 '/{0}/config/logger'.format(version))
api.add_resource(Config_Monitor_App_Boundary,
                 '/{0}/config/monitor'.format(version))
api.add_resource(Config_Pair_Boundary,
                 '/{0}/config/pair'.format(version))
api.add_resource(Config_Push_Notifications_Boundary,
                 '/{0}/config/push'.format(version))
api.add_resource(Config_Unlock_Boundary,
                 '/{0}/config/unlock'.format(version))
api.add_resource(Config_Context_Boundary,
                 '/{0}/config/context'.format(version))
