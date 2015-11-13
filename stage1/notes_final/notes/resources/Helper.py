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
from collections import OrderedDict

class Helper(Resource):
    def get(self):
        action_list = []
        links = OrderedDict({'_links':{}})

        with app.test_request_context():
            notifications = Notifications()
            notification_list = notifications.get()

            if notification_list == None:
                notification_list = []

            links['_links']['self'] = {
                'href':Config.make_url(Helper, _external=True),
                'rel':'self',
                'description':'Display routes supported by this service.'}
            links['_links']['notifications'] = {
                'href':Config.make_url(Notifications, _external=True),
                'rel':'notifications',
                'description':'The set of notifications.'}

            if 'notifications' in notification_list:
                for note in notification_list['notifications']:
                    links['_links']['notifications'+\
                            str(note['identifier'])] = {
                        'href':note['_links']['_self'],
                        'rel':'notification',
                        'description':'Notification ' + \
                         str(note['identifier'])}

            links['_links']['lock'] = {
                'href':Config.make_url(Lock, _external=True),
                'rel':'lock',
                'description':'Lock device.'}
            links['_links']['unlock'] = {
                'href':Config.make_url(Unlock, unlock_code=9999, _external=True),
                'rel':'unlock',
                'description':'Unlock device, replacing 9999 with lock code'}

        return links


