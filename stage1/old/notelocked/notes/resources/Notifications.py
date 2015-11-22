from notes import app,api
from flask_restful import Resource, request, reqparse
from flask import abort, url_for
import notes.resources.Config as Config
import sys

class Notifications(Resource):
    def get(self):
        if (Config.locked):
            return None

        return_list = []

        try:
            if len(Config.notificationList) > 0:
                for idx, note in enumerate(Config.notificationList):
                    temp_dict = []
                    temp_dict = {'sensitivity':note['sensitivity']}
                    temp_dict['note'] = note['note']
                    if not Config.locked:
                        temp_dict['_link'] = api.url_for(NotificationGetter, id = idx)

                    return_list.append(temp_dict)
        except Exception as e:
            return {'error':repr(e)}
            #abort(400)
        
        return {'notifications': return_list}

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
        except Exception as e:
            return {'error':repr(e)}

    def put(self, id):
        try:
            updated_data = False
            parser = reqparse.RequestParser()
            parser.add_argument('note', type=str)
            parser.add_argument('action', type=str)
            parser.add_argument('sensitivity', type=str)
            args = parser.parse_args()

            for k, v in args.items():
                if k.upper() in ['NOTE', 'ACTION', 'SENSITIVITY']:
                    if not v == None:
                        Config.notificationList[id][k] = v
                        updated_data = True
                else:
                    raise ValueError('Unexpected paramter passed to /notification/9 >>> ' + k)

            if updated_data:
                if str(args['sensitivity']).upper() == 'HIGH' \
                and Config.locked:
                    return None
                return(Config.notificationList[id])
            else:
                raise ValueError('No data to update or paramters incorrectly parsed.')
        except IndexError:
            abort(404)
        except ValueError:
            abort(400)
        except Exception as e:
            return {'error':repr(e)}

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
            parser.add_argument(
                'sensitivity',
                type=str
            )
            args = parser.parse_args()

            Config.notificationList.append({
                    'note':args['note'],
                    'action':args['action'],
                    'sensitivity':args['sensitivity']
                }
            )
            if str(args['sensitivity']).upper() == 'HIGH' \
            and Config.locked:
                return None
            return {'notification sent':Config.notificationList[-1:]}
        except Exception as e:
            return {'error':repr(e)}
