from notes import app,api
from flask_restful import Resource, request, reqparse
from flask import abort, url_for
import notes.resources.Config as Config
import sys

class Notifications(Resource):
    def get(self):
        returnList = []
        for idx, note in enumerate(Config.notificationList):
            #from app import api
            temp_dict = {'note':note['note']}
            if not Config.locked:
                temp_dict['_link'] = api.url_for(NotificationGetter, id = idx)
            returnList.append(temp_dict)
        
        return {'notifications':returnList}

class NotificationsClear(Resource):
    def put(self):
        Config.notificationList = []
        return {'notifications':Config.notificationList}

class NotificationGetter(Resource):
    def get(self, id):
        try:
            if Config.locked:
                return {'notice':'unlock device first'}
            return Config.notificationList[id]
        except IndexError:
            abort(404)
        except:
            return {'error':str(sys.exc_info()[0])}

    def put(self, id):
        try:
            updated_data = False
            parser = reqparse.RequestParser()
            parser.add_argument('note', type=str)
            parser.add_argument('action', type=str)
            args = parser.parse_args()

            for k, v in args.items():
                if k.upper() in ['NOTE','ACTION'] \
                and not v == None:
                    Config.notificationList[id][k] = v
                    updated_data = True
                else:
                    abort(400)

            if updated_data:
                return(Config.notificationList[id])
            else:
                abort(400)
        except IndexError:
            abort(404)
        except Exception as e:
            abort(400)
            #return {'error':repr(e)}
            #return {'error':str(sys.exc_info().message)}

class NotificationAdder(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'note',
                type=str,
                required=True,
                help='You must provide a message for the notification'
            )
            parser.add_argument(
                'action',
                type=str,
                required=True,
                help='You must provide an action'
            )
            args = parser.parse_args()

            Config.notificationList.append({
                    'note':args['note'],
                    'action':args['action']
                }
            )
            return {'notification sent':Config.notificationList[-1:]}
        except:
            return {'error':str(sys.exc_info()[0])}
