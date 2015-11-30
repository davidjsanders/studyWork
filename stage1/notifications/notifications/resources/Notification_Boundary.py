from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

from notifications.resources.Notification import Notification
from notifications.resources.Response import Response_Object
from notifications.resources.Notification_DB import Notification_DB
#from notifications.resources.Config import __is_locked
import notifications.resources.Config as Config

from jsonschema import exceptions
import json

class Notification_All(Resource):
    database_name = 'datavol/notifications.db'

    def get(self, controlkey=None):
        try:
            raw_list=[]
            return_list = []
            return_dict = ''
            schema_context={}

            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            if Config.check_key('locked'):
                if Config.check_key('pre-lollipop'):
                    raise RuntimeError('Device is locked.')
                else:
                    schema_context={'locked':True}
                    if Config.check_key('android'):
                        schema_context['android'] = True

                # Otherwise set the context to not show sensitive notifications
                #

            return_message = 'success'
            return_status = 200
            return_success_fail = 'success'

            noteDB = Notification_DB()
            raw_list = noteDB.query_all()

            for row in raw_list:
                note = Notification()
                note.load(row)

                try:
                    appending_note = json.loads(
                        note.dump(
                            schema_context=schema_context
                        )
                    )
                    return_list.append(appending_note)
                except exceptions.ValidationError as ve:
                    pass # A validate error means ignore, don't pass data back
                except Exception:
                    raise # Something else happened, so inform caller

            if return_list == []:
                return_message = 'No notifications.'
            else:
                return_message = 'notifications found'
        except exceptions.ValidationError as ve:
            return_message = ve.message
            return_status = 400
            return_success_fail = 'error'
        except RuntimeError as re:
            return_message = str(re)
            return_status = 403
            return_success_fail = 'error'
        except Exception as e:
            return_message = repr(e)
            return_status = 400
            return_success_fail = 'error'

        return Response_Object(
                return_list,
                return_status,
                return_success_fail,
                return_message
            ).response()

    def delete(self, controlkey=None):
        return_message = 'Notifications deleted'
        return_status = 200
        return_success_fail = 'success'

        try:
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            noteDB = Notification_DB()
            noteDB.delete_all()
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not deleted. '+\
                repr(e)}
            return_success_fail = 'error'
        
        return Response_Object(
                [],
                return_status,
                return_success_fail,
                return_message
            ).response()


    def post(self, controlkey=None):
        return_data = []
        return_message = ''
        return_status = 201
        return_success_fail = ''

        try:
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            raw_json = reqparse.request.get_data().decode('utf-8')
            json_data = json.loads(raw_json)
            note = Notification()
            note.load(raw_json)

            noteDB = Notification_DB()
            noteDB.insert(note)

            return_message = 'Notification created'
            return_data = note.dump()
            return_success_fail = 'success'
        except exceptions.ValidationError as ve:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                str(ve)}
            return_success_fail = 'error'
            return_data = []
        except KeyError as ke:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                str(ke) + '. No valid key found in: ' +\
                reqparse.request.get_data().decode('utf-8')}
            return_success_fail = 'error'
            return_data = []
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                repr(e)}
            return_success_fail = 'error'
            return_data = []

        return Response_Object(
            return_data,
            return_status,
            return_success_fail,
            return_message
        ).response()

class Notification_One(Resource):
    database_name = 'datavol/notifications.db'
    return_dict = {}

    def get(self, id, controlkey=None):
        try:
            return_list = []
            return_string = ''
            return_message = ''
            return_status = 200
            return_success_fail = ''
            schema_context={}

            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            if Config.check_key('locked'):
                if Config.check_key('pre-lollipop'):
                    raise RuntimeError('Device is locked.')
                else:
                    schema_context={'locked':True}
                    if Config.check_key('android'):
                        schema_context['android'] = True

            noteDB = Notification_DB()
            note = Notification()
            note.load(noteDB.query_one(id))

            try:
                appending_note = json.loads(
                    note.dump(
                        schema_context=schema_context
                    )
                )
                return_list.append(appending_note)
            except exceptions.ValidationError as ve:
                pass # A validate error means ignore, don't pass data back
            except Exception:
                raise # Something else happened, so inform caller

            if return_list == []:
                if 'android' in schema_context\
                and 'locked' in schema_context:
                    return_message = 'Notification is sensitive and cannot '+\
                        'be displayed because device is locked.'
                    return_status = 403
                else:
                    return_message = 'Notification not found.'
                    return_status = 404
                return_success_fail = 'error'
            else:
                return_message = 'success'
                return_status = 200
                return_success_fail = 'success'
        except IndexError as ie:
            return_message = 'The notification '+str(id)+' does not exist.'
            return_status = 404
            return_success_fail = 'error'
        except exceptions.ValidationError as ve:
            pass
        except RuntimeError as re:
            return_message = str(re)
            return_status = 403
            return_success_fail = 'error'
        except Exception as e:
            return_message = repr(e)
            return_status = 400
            return_success_fail = 'error'
            return_status = 400
        
        return Response_Object(
                return_list,
                return_status,
                return_success_fail,
                return_message
            ).response()

    def put(self, id, controlkey=None):
        return_data = []
        return_message = ''
        return_status = 200
        return_success_fail = ''

        try:
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            noteDB = Notification_DB()
            note = Notification()
            note.load(noteDB.query_one(id))
            temp = Notification()

            raw_json = reqparse.request.get_data().decode('utf-8')
            new_note = json.loads(raw_json)

            for key in new_note.keys():
                if key == 'note':
                    note.note = new_note[key]
                elif key == 'action':
                    note.action = new_note[key]
                elif key == 'sensitivity':
                    note.sensitivity = new_note[key]
                elif key == 'identifier':
                    pass
                else:
                    temp.load(raw_json) # Force a validation error
            temp.load(note.dump())

            noteDB.update_one(note.identifier, note.dump())

            return_message = 'Notification updated.'
            return_data = note.dump()
            return_success_fail = 'success'
        except IndexError as ie:
            return_message = 'The notification '+str(id)+' does not exist.'
            return_status = 404
            return_success_fail = 'error'
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                repr(e)}
            return_success_fail = 'error'
            return_data = []
        
        return Response_Object(
                return_data,
                return_status,
                return_success_fail,
                return_message
            ).response()

    def delete(self, id, controlkey=None):
        try:
            return_data = []
            return_message = ''
            return_status = 200
            return_success_fail = ''

            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            noteDB = Notification_DB()
            note = Notification()
            note.load(noteDB.query_one(id))
            noteDB.delete_one(id)

            return_message = 'Notification deleted'
            return_success_fail = 'success'
        except IndexError as ie:
            return_message = 'The notification '+str(id)+' does not exist.'
            return_status = 404
            return_success_fail = 'error'
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                repr(e)}
            return_success_fail = 'error'
            return_data = []
        
        return Response_Object(
                return_data,
                return_status,
                return_success_fail,
                return_message
            ).response()


