from notes import app,api
from flask_restful import Resource, request, reqparse
from flask import abort
from notes.resources.Notifications \
    import Notifications, \
           NotificationAdder
from notes.resources.Lock \
    import Lock, Unlock
import sqlite3
import requests
import notes.resources.Config as Config
import sys

class Helper(Resource):
    def get(self):
        action_list = []

        with app.test_request_context():
            notifications = Notifications()
            notification_list = notifications.get()
            if notification_list == None:
                notification_list = []

            action_list.append({
                'href':Config.make_url(Helper, _external=True),
                'rel':'self',
                'method':'GET',
                'description':'Display routes available.'})
            action_list.append({
                'href':Config.make_url(Notifications, _external=True),
                'rel':'notifications',
                'method':'GET',
                'description':'Display notifications.'})
            action_list.append({
                'href':Config.make_url(NotificationAdder, _external=True),
                'rel':'notification',
                'method':'POST',
                'description':'Add a new notification.',
                'comment':'{\'note\':\'<str:note>\', '+ \
                     '\'action\':\'<str:action>\'}'})

            if 'notifications' in notification_list:
                for note in notification_list['notifications']:
                    action_list.append({
                        'href':note['_links']['_self'],
                        'method':['GET','PUT','DELETE'],
                        'description':'Get notification ' + \
                         str(note['identifier'])
                    })
#                action_list.append({
#                     'href':note['href'],
#                      'method':'PUT',
#                      'description':'Update notification ' + str(note['id']),
#                      'comment':'{\'note\':\'<str:note>\', '+ \
#                          '\'action\':\'<str:action>\'}'
#                    })

            action_list.append({
                'href':Config.make_url(Lock, _external=True),
                'rel':'lock',
                'method':'GET',
                'description':'Get device locked status.'})
            action_list.append({
                'href':Config.make_url(Lock, _external=True),
                'rel':'lock',
                'method':'PUT',
                'description':'Lock the device.'})
            action_list.append({
                'href':Config.make_url(Unlock, unlock_code=9999, _external=True),
                'rel':'unlock',
                'method':'PUT',
                'description':'Unlock the device with the code 9999.'})
            links = {'_links':action_list}
        return links


