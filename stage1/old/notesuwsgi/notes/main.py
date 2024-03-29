from flask_restful import Resource, Api
from notes import app, api

import notes.resources.Config as Config
from notes.resources.Notifications \
    import Notifications, \
           NotificationsClear, \
           NotificationGetter, \
           NotificationAdder
from notes.resources.Lock import Lock, Unlock

class Helper(Resource):
    def get(self):
        action_list = []

        with app.test_request_context():
            notifications = Notifications()
            notification_list = notifications.get()

            action_list.append({
                'href':api.url_for(Helper),
                'rel':'self',
                'method':'GET',
                'description':'Display routes available.'})
            action_list.append({
                'href':api.url_for(Notifications),
                'rel':'notifications',
                'method':'GET',
                'description':'Display notifications.'})
            action_list.append({
                'href':api.url_for(NotificationAdder),
                'rel':'notification',
                'method':'POST',
                'description':'Add a new notification.',
                'comment':'{\'note\':\'<str:note>\', '+ \
                     '\'action\':\'<str:action>\'}'})

            for note in notification_list['notifications']:
                action_list.append({
                     'href':note['href'],
                      'method':['GET','PUT','DELETE'],
                      'description':'Get notification ' + str(note['id'])
                    })
#                action_list.append({
#                     'href':note['href'],
#                      'method':'PUT',
#                      'description':'Update notification ' + str(note['id']),
#                      'comment':'{\'note\':\'<str:note>\', '+ \
#                          '\'action\':\'<str:action>\'}'
#                    })

            action_list.append({
                'href':api.url_for(Lock),
                'rel':'lock',
                'method':'GET',
                'description':'Get device locked status.'})
            action_list.append({
                'href':api.url_for(Lock),
                'rel':'lock',
                'method':'PUT',
                'description':'Lock the device.'})
            action_list.append({
                'href':api.url_for(Unlock, unlock_code=9999),
                'rel':'unlock',
                'method':'PUT',
                'description':'Unlock the device with the code 9999.'})
            links = {'_links':action_list}
        return links

api.add_resource(Notifications, '/notifications')
api.add_resource(NotificationGetter, '/notification/<int:id>')
api.add_resource(NotificationAdder, '/notification')
api.add_resource(NotificationsClear, '/clear')
api.add_resource(Lock, '/lock')
api.add_resource(Unlock, '/unlock/<int:unlock_code>')
api.add_resource(Helper, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
