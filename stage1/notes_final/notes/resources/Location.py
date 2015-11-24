from notes import app,api
from flask_restful import Resource, request, reqparse, url_for
from flask import abort
import requests
import notes.resources.Config as Config
import notes.resources.Notifications as Notifications
import sys

class Location(Resource):
    def get(self):
        return {'location':'(123.21, 232.11)'}

class Hotspot(Resource):
    def post(self, hot_text):
        pass
        #notification_center = Notifications.NotificationAdder()
        #notification_center.post()
