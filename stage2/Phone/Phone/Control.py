from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone.Phone_Database import Phone_Database

import datetime, time, json, os

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = 'datavolume/Log_File.txt'
    __phone_db = None

    __server_name=None
    __port_number=0


    def __init__(self):
        # Get hostname and port from OS. If the environment variables have not
        # been set, e.g. the app is being run locally, then catch an exception
        # and default to Flask's built-in server, localhost on port 5000.
        #
        stage = 0      # A stage indicator to know which variable caused the
                       # exception
        try:
            stage += 1
            port_number = os.environ['portToUse']
            stage += 1
            server_name = os.environ['serverName']
        except KeyError as ke:
            if stage == 1:
                port_number = 5000
                server_name = 'localhost'
            else:
                server_name = 'localhost'

        self.__server_name = server_name
        self.__port_number = port_number

        self.__phone_db = Phone_Database(self.__server_name,
                                         self.__port_number)

        self.__phone_db.set_key('server_name', server_name)
        self.__phone_db.set_key('port_number', port_number)
        self.__phone_db.set_key('phonename', server_name+'_'+str(port_number))
        self.__phone_db.set_key('output_device',
           'datavolume/onscreen_notifications-'+server_name+\
           '-'+str(port_number)+'.txt'
        )


    def get_value(self, key=None):
        if key == None:
            return None

        return self.__phone_db.get_key(key)


    def set_value(self, key=None, value=None):
        if key == None:
            return None

        return self.__phone_db.set_key(key, value)


    def clear_value(self, key=None):
        if key == None:
            return None

        return self.__phone_db.clear_key(key)


    def persist_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        self.__phone_db.save_notification(
            sender,
            date_string,
            notification,
            action
        )


    def get_bluetooth(self):
        return self.__phone_db.get_bluetooth_device()


    def set_bluetooth(self, devicename=None):
        return self.__phone_db.set_bluetooth_device(devicename)


    def log(self,
            log_message=None
    ):
        now = datetime.datetime.now()
        f = None
        try:
            f = open(self.__log_file, 'a')
            f.write('{0}: {1}'.format(now,log_message)+"\n")
        except Exception:
            raise
        finally:
            if not f == None:
                f.close()

    def do_response(self,
                    status=200,
                    response='success',
                    data=None,
                    message=''):
        return_dict = {"status":status,
                       "response":response,
                       "data":data,
                       "message":message}
        return Response(
            json.dumps(return_dict),
            status=status,
            mimetype='application/json')


#
# Version 1.00
# ----------------------------------------------------------------------------
# 30 Jan 2016: Updated to add multiple devices based on server name and port
#
class Control_v1_00(Control):
    def future(self):
        pass

