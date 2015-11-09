from notes import app,api
from flask_restful import Resource
from flask import request
from marshmallow import Schema, fields, ValidationError
import sqlite3
import notes.resources.Config as Config
from notes.resources.Persist import Persistance

class Notifications(Resource):
    def get(self):
        try:
            notification_list = []
            persist = Persistance()
            for db_row in persist.fetch_all(Config.database_connection):
                notification = Config.Note()
                notification.load(db_row[0], NotificationGetter, Notifications)

                append_notification = False

                if Config.enable_sensitivity:
                    if not Config.locked:
                        append_notification = True
                    elif notification.privacy_check():
                        append_notification = True
                else:
                    append_notification = True

                if append_notification:
                    notification_list.append(notification.json())
        except Exception as e:
            return {'error':repr(e)}
        
        return {'notifications':notification_list}

    def delete(self):
        persist = Persistance()
        return persist.clear_all(Config.database_connection)

class NotificationGetter(Resource):
    def get(self, id):
        if Config.locked:
            return {'notice':'unlock device first'}
        try:
            notification = Config.Note()
            notification.load(id, NotificationGetter, Notifications)
            return_list = {'notification':notification.json()}
        except Exception as e:
            return_list = {'error':repr(e)}
        
        return return_list

    def put(self, id):
        try:
            return_list = []

            existing_notification = Config.Note()
            existing_notification.load(id, NotificationGetter, Notifications)

            new_data = Config.NoteSchema(strict=False).load(request.get_json()).data

            existing_notification.update(new_data)
            existing_notification.save()
            return_list = existing_notification.json()
        except Exception as e:
            return_list = {'error':repr(e)}, 400

        return return_list

    def delete(self, id):
        try:
            notification = Config.Note()
            notification.load(id, NotificationGetter, Notifications)
            notification.delete()
            notification = Config.Note()
        except ValidationError as e:
            return {'error':repr(e)}, 400
        except Exception as e:
            return {'error':repr(e)}, 400

        return {'notification':[]}

class NotificationAdder(Resource):
    def post(self):
        try:
            notification = Config.NoteSchema(strict=True) \
                .load(request.get_json()).data
            notification.save()
            notification.define_links(
                NotificationGetter,
                Notifications)
        except ValidationError as e:
            return {'error':repr(e)}, 400
        except Exception as e:
            return {'error':repr(e)}, 400

        return {'full':notification.json()}


