from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Logger.Logger_Database import Logger_Database

import datetime, time, json, os
from textwrap import wrap

class Control(object):
    __log_file = None
    __logger_db = None

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
            stage += 1
            host_ip = os.environ['hostIP']
            stage += 1
            version = os.environ['version']
        except KeyError as ke:
            if stage == 1:
                port_number = 5000
                server_name = 'localhost'
            elif stage == 2:
                server_name = 'localhost'
            elif stage == 3:
                host_ip = '127.0.0.1'
            else:
                version = 'v1_00'

        self.__logger_db = \
            Logger_Database(server_name, port_number)

        self.__log_file = 'datavolume/'+server_name+'-'+str(port_number)+\
            '-log.txt'
        self.file_clear()

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting server_name to {0}'.format(server_name),
                 timestamp=str(datetime.datetime.now()))
        self.__server_name = server_name

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting port number to {0}'.format(port_number),
                 timestamp=str(datetime.datetime.now()))
        self.__port_number = port_number

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting Host IP Address to {0}'.format(host_ip),
                 timestamp=str(datetime.datetime.now()))
        self.__host_ip = host_ip

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting version to {0}'.format(version),
                 timestamp=str(datetime.datetime.now()))
        self.__version = version


    def get_version(self):
        return self.__version


    def delete_log(self):
        self.file_clear()
        return self.__logger_db.clear_log()


    def get_log(self, sender=None):
        if sender == None:
            return self.__logger_db.get_log()
        else:
            return self.__logger_db.get_log_by_sender(sender)


    def log(self,
            sender=None,
            log_type=None,
            message=None,
            timestamp=None
    ):
        now = str(datetime.datetime.now())
        try:
            self.file_log('{0},{1},{2},{3}'\
                .format(sender,log_type,message,timestamp))
        except Exception as e:
            print('FILE LOG: Unknown exception! {0}'.format(repr(e)))

        try:
            self.__logger_db.write_log(sender, log_type, message, timestamp)
        except Exception as e:
            print('DB LOG: Unknown exception! {0}'.format(repr(e)))


    def file_log(self, log_message=None):
        f = None
        try:
            f = open(self.__log_file, 'a')
            f.write('{0}'.format(log_message+"\n"))
        except Exception as e:
            raise
        finally:
            if not f == None:
                f.close()


    def file_clear(self):
        now = str(datetime.datetime.now())
        f = None
        try:
            f = open(self.__log_file, 'w')
            f.write('{0},{1},{2},{3}'\
                .format("LOGGER","INITIALIZE","Log file created.",now)+"\n")
        except Exception as e:
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


    def write_console(self, message=None):
        if message == None:
            return

        print(message)


    def print_error(self, error_message=None):
        print('{0}'.format('-'*80))
        print('*** {0} ***'.format(error_message))
        print('{0}'.format('-'*80))

global_control = Control()
