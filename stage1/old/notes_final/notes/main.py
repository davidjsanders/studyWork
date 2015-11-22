from flask_restful import Resource, Api
from notes import app, api

import notes.resources.Config as Config
from notes.resources.Notifications \
    import Notifications, \
           NotificationsID
from notes.resources.Helper \
    import Helper
from notes.resources.Lock \
    import Lock, \
           Unlock
from notes.resources.Mode \
    import Modes, \
           ModesGet

api.add_resource(Notifications, '/v1_01/notifications')
api.add_resource(NotificationsID, '/v1_01/notifications/<int:id>')
#api.add_resource(NotificationAdder, '/notifications')
api.add_resource(Lock, '/v1_01/lock')
api.add_resource(Unlock, '/v1_01/unlock/<int:unlock_code>')
api.add_resource(Helper, '/v1_01/', '/')
api.add_resource(Modes, '/v1_01/modes/<int:mode>')
api.add_resource(ModesGet, '/v1_01/modes')

#print('In Configuration.')
#Config.initialize()
