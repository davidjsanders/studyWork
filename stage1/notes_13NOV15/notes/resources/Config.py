"""
This module contains key configuration variables used throughout
the package.
"""

from notes import app,api
from flask import url_for
from marshmallow import Schema, fields, post_load
from notes.resources.Persist import Persistance, Configuration
import sqlite3
#
# Added - 07 Nov 2015
#

database_connection = 'datavol/notesuwsgi.db'
locked = False
unlock_code = 1234

app_mode = 2
app_mode_no_notifications = 1
app_mode_all_notifications = 2
app_mode_no_sensitive = 3

enable_sensitivity = True
testing_enabled = False
port_number = 5000

def make_url(*args, **kwargs):
    url = api.url_for(*args, **kwargs)
    return url.replace('://localhost/','://localhost:'+str(port_number)+'/')

def initialize():
    database_opened = False
    try:
        db_connection = sqlite3.connect(database_connection)
        database_opened = True
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            'delete from configuration '+ \
            'where port = ?', \
            (port_number,)
        )
        db_connection.commit()
        db_cursor.execute(
            'insert into configuration '+ \
            'values (?, ?, ?)', \
            (port_number, 'mode', app_mode)
        )
        db_connection.commit()
        db_cursor.execute(
            'insert into configuration '+ \
            'values (?, ?, ?)', \
            (port_number, 'locked', False)
        )
        db_connection.commit()
    except Exception as e:
        raise e
    finally:
        if database_opened:
            db_cursor.close()
            db_connection.close()

def set_app_mode(mode):
    try:
        con = Configuration()
        con.set_mode(mode, port_number, database_connection)
    except Exception as e:
        return {'error':repr(e)}

def get_app_mode():
    try:
        con = Configuration()
        return con.get_mode(port_number, database_connection)
    except Exception as e:
        return {'error':repr(e)}

def set_lock(lock_status):
    try:
        con = Configuration()
        return con.set_lock(lock_status, port_number, database_connection)
    except Exception as e:
        return {'error':repr(e)}

def get_lock():
    try:
        con = Configuration()
        return con.get_lock(port_number, database_connection)
    except Exception as e:
        return {'error':repr(e)}

class Note(object):
    def __init__(self, note=None, action=None, sensitivity=None, dummy='Ignore'):
        try:
            self._saved = False
            self.identifier = None
            self._links = {'_self':None, '_collection':''}
            self.note = note
            self.action = action
            self.sensitivity = sensitivity
        except Exception as e:
            raise e

    def __repr__(self):
        return '<Note(identifier={self.identifier!r}>'.format(self=self)

    def privacy_check(self):
        if self.sensitivity.upper() == 'HIGH':
            return False
        else:
            return True

    def json(self):
        return NoteSchema().dump(self)[0]

    def set_identifier(self, idvalue):
        if idvalue > 0:
            self.identifier = idvalue
        else:
            raise ValueError('ID must be greater than zero.')

    def define_links(self, notificationGetter, notifications):
        try:
            if self.identifier == None \
            or notificationGetter == None \
            or notifications == None:
                raise ValueError('A required value for define_links is missing!')
            self._links['_self'] = make_url(
                notificationGetter,
                id = self.identifier,
                _external=True)
            self._links['_collection'] = make_url(
                notifications,
                _external=True)
        except Exception as e:
            raise e

    def load(self, id, getter, collection):
        try:
            self.set_identifier(id)
            persist = Persistance()
            temp = persist.fetch_one(
                db_connection = database_connection,
                identifier = self.identifier)
            self.note = temp['note']
            self.action = temp['action']
            self.sensitivity = temp['sensitivity']
            self.define_links(getter, collection)
            self._saved = True
        except Exception as e:
            raise e

    def update(self, updated_notification):
        if 'NOTE' in str(updated_notification).upper():
            self.note = updated_notification['note']
        if 'ACTION' in str(updated_notification).upper():
            self.action = updated_notification['action']
        if 'SENSITIVITY' in str(updated_notification).upper():
            self.sensitivity = updated_notification['sensitivity']

    def delete(self):
        try:
            persist = Persistance()
            persist.delete(
                notification = self,
                db_connection = database_connection)
        except Exception as e:
            raise e

    def save(self):
        try:
            if self._saved:
                self.__update()
            else:
                self._saved = True
                self.__insert()
        except Exception as e:
            raise e

    def __update(self):
        try:
            persist = Persistance()
            persist.update(
                notification = self,
                db_connection = database_connection)
        except Exception as e:
            raise e

    def __insert(self):
        persist = Persistance()
        self.identifier = persist.insert(
            notification = self,
            db_connection = database_connection)

        

class NoteSchema(Schema):
    identifier = fields.Integer()
    _links = fields.Dict()
    note = fields.Str(required=True)
    action = fields.Str(required=True)
    sensitivity = fields.Str(required=True)

    @post_load
    def make_Note(self, data):
        note = Note(**data)
        return note

