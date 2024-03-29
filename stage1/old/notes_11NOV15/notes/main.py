from flask_restful import Resource, Api
from notes import app, api

import notes.resources.Config as Config
from notes.resources.Notifications \
    import Notifications, \
           NotificationGetter, \
           NotificationAdder
from notes.resources.Helper \
    import Helper
from notes.resources.Lock \
    import Lock, \
           Unlock
from notes.resources.Mode \
    import Mode, \
           ModeGet

api.add_resource(Notifications, '/notifications')
api.add_resource(NotificationGetter, '/notification/<int:id>')
api.add_resource(NotificationAdder, '/notification')
api.add_resource(Lock, '/lock')
api.add_resource(Unlock, '/unlock/<int:unlock_code>')
api.add_resource(Helper, '/')
api.add_resource(Mode, '/mode/<int:mode>')
api.add_resource(ModeGet, '/mode')

#print('In Configuration.')
#Config.initialize()
