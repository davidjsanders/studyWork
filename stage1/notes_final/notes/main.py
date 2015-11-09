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

api.add_resource(Notifications, '/notifications')
api.add_resource(NotificationGetter, '/notification/<int:id>')
api.add_resource(NotificationAdder, '/notification')
api.add_resource(Lock, '/lock')
api.add_resource(Unlock, '/unlock/<int:unlock_code>')
api.add_resource(Helper, '/')

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True)
