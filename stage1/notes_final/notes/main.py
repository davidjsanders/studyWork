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

api.add_resource(Notifications, '/notifications')
api.add_resource(NotificationsID, '/notifications/<int:id>')
#api.add_resource(NotificationAdder, '/notifications')
api.add_resource(Lock, '/lock')
api.add_resource(Unlock, '/unlock/<int:unlock_code>')
api.add_resource(Helper, '/')
api.add_resource(Modes, '/modes/<int:mode>')
api.add_resource(ModesGet, '/modes')

#print('In Configuration.')
#Config.initialize()
