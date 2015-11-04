#!/flask/bin/python3
from flask import Flask, Blueprint, abort
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

import resources.Config as Config
from resources.Notifications \
    import Notifications, NotificationGetter, NotificationAdder
from resources.Lock import Lock, Unlock

class Helper(Resource):
    def get(self):
        action_list = []
        with app.test_request_context():
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
                'comment':'expects json data...'})
            for idx, note in enumerate(Config.notificationList):
                action_list.append({
                     'href':api.url_for(NotificationGetter, id = idx),
                      'method':'GET',
                      'description':'Get notification ' + str(idx),
                      'comment':'expects json data in a field called "note"'
                    })
                action_list.append({
                     'href':api.url_for(NotificationGetter, id = idx),
                      'method':'PUT',
                      'description':'Update notification ' + str(idx),
                      'comment':'expects json data in a field called "note"'
                    })
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
api.add_resource(Lock, '/lock')
api.add_resource(Unlock, '/unlock/<int:unlock_code>')
api.add_resource(Helper, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
