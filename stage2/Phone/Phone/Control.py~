from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone.Phone_Database import Phone_Database

import datetime, time, json, os, redis
from textwrap import wrap

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = None
    __phone_db = None
    __redis = {'host':'localhost', 'port':6379, 'db':0}

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
        self.__log_file = 'datavolume/'+server_name+'-'+\
                          str(port_number)+'/log.txt'

        self.__phone_db.set_key('server_name', server_name)
        self.__phone_db.set_key('port_number', port_number)
        self.__phone_db.set_key('phonename', server_name+'_'+str(port_number))
        self.__phone_db.set_key('output_device',
           'datavolume/'+server_name+'-'+str(port_number)+\
           '/onscreen_notifications-'+server_name+\
           '-'+str(port_number)+'.txt'
        )
        self.log('*'*78)
        self.log('{0}:{1} Started'.format(server_name, port_number))
        self.log('*'*78)
        self.log()


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


    def write_screen(self, output_line=None):
        if output_line == None:
            return
        redis_instance = redis.StrictRedis(**self.__redis)
        return redis_instance.publish(
            'output_screen',
            '{0}\n'.format(output_line)
            )


    def log(self,
            log_message=None
    ):
        now = datetime.datetime.now()
        f = None
        try:
            f = open(self.__log_file, 'a')
            if log_message == None or log_message == '':
                f.write("{0:>28s}\n".format(str(now)+': '))
                self.write_screen("\n")
            else:
                wrapped80 = wrap(log_message, 79)
                time_line = [str(now)]
                for line in wrapped80:
                    time_line.append('')
                for i, line in enumerate(wrapped80):
                    f.write('{0:>28s}{1}'.format(time_line[i]+': ', line)+"\n")
                for line in wrapped80:
                    self.write_screen(line+"\n")
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


global_controller = Control()

