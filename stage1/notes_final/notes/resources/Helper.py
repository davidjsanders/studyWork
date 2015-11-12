from notes import app,api
from flask_restful import Resource, request, reqparse
from flask import abort
from notes.resources.Notifications \
    import Notifications
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
                'description':'Routes.'})
            action_list.append({
                'href':Config.make_url(Notifications, _external=True),
                'rel':'notifications',
                'description':'Notifications.'})

            if 'notifications' in notification_list:
                for note in notification_list['notifications']:
                    action_list.append({
                        'href':note['_links']['_self'],
                        'rel':'_self',
                        'description':'Notification ' + \
                         str(note['identifier'])
                    })

            action_list.append({
                'href':Config.make_url(Lock, _external=True),
                'rel':'lock',
                'description':'Lock device.'})
            action_list.append({
                'href':Config.make_url(Unlock, unlock_code=9999, _external=True),
                'rel':'unlock',
                'description':'Unlock device, replace 9999'})
            links = {'_links':action_list}
        return links


