"""
This module contains key configuration variables used throughout
the package.
"""

from notes import app,api
from flask import url_for
from marshmallow import Schema, fields, post_load
from notes.resources.Persist import Persistance
#
# Added - 07 Nov 2015
#

database_connection = 'datavol/notesuwsgi.db'
locked = False
unlock_code = 1234
enable_sensitivity = True
testing_enabled = False

class Note(object):
    def __init__(self, note=None, action=None, sensitivity=None):
        self._saved = False
        self.identifier = None
        self._links = {'_self':None, '_collection':''}
        self.note = note
        self.action = action
        self.sensitivity = sensitivity

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
            self._links['_self'] = api.url_for(
                notificationGetter,
                id = self.identifier,
                _external=True)
            self._links['_collection'] = api.url_for(
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
        return Note(**data)

