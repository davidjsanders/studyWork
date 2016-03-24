# Import base library modules - From Bluetooth symbolic link to /base_lib
import base_lib
from base_lib.Environment import Environment

from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Logger.Logger_Database import Logger_Database

import datetime, time, json, os
from textwrap import wrap

class v3_00_Control(object):
    log_file = None
    root = None
    logger_db = None

    def __init__(self):
        # Setup environment
        self.environment = Environment()
        port_number = self.environment['port_number']
        server_name = self.environment['server_name']
        host_ip = self.environment['ip_addr']
        version = self.environment['version']

        self.logger_db = \
            Logger_Database(server_name, port_number)

        self.root = '/Logger'
        self.log_file = 'datavolume/'+server_name+'-'+str(port_number)+\
            '-log.txt'
        self.file_clear()

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting server_name to {0}'.format(server_name),
                 timestamp=str(datetime.datetime.now()))
        self.server_name = server_name

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting port number to {0}'.format(port_number),
                 timestamp=str(datetime.datetime.now()))
        self.port_number = port_number

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting Host IP Address to {0}'.format(host_ip),
                 timestamp=str(datetime.datetime.now()))
        self.host_ip = host_ip

        self.log(sender='LOGGER',
                 log_type='INTERNAL',
                 message='Setting version to {0}'.format(version),
                 timestamp=str(datetime.datetime.now()))
        self.version = version


    def get_version(self):
        return self.version


    def get_log_filename(self):
        return '{0}/{1}'.format(self.root, self.log_file)


    def delete_log(self):
        self.file_clear()
        return self.logger_db.clear_log()


    def get_log(self, sender=None):
        if sender == None:
            return self.logger_db.get_log()
        else:
            return self.logger_db.get_log_by_sender(sender)


    def log(self,
            sender=None,
            log_type=None,
            message=None,
            timestamp=None
    ):
        now = str(datetime.datetime.now())
        if not timestamp == None:
            now = timestamp

        try:
            self.file_log('"{0}","{1}","{2}","{3}"'\
                .format(now,sender,log_type,message))
        except Exception as e:
            print('FILE LOG: Unknown exception! {0}'.format(repr(e)))

        try:
            self.logger_db.write_log(sender, log_type, message, now)
        except Exception as e:
            print('DB LOG: Unknown exception! {0}'.format(repr(e)))


    def file_log(self, log_message=None):
        f = None
        try:
            f = open(self.log_file, 'a')
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
            f = open(self.log_file, 'w')
            f.write('{0},{1},{2},{3}'\
                .format("Timestamp", "Sender", "Log Type", "Activity")+"\n")
            f.write('{0},{1},{2},{3}'\
                .format(now, "logger", "initialize", "Log file created.")+"\n")
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


