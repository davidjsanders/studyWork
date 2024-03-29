from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import Pairing_Database

import datetime, time, json, os, requests
from textwrap import wrap

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = None
    __pairing_db = None

    def __init__(self):
        stage = 0
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

        self.__server_name = server_name
        self.__port_number = port_number

        self.__pairing_db = Pairing_Database.Pairing_Database(
            server_name = self.__server_name,
            port_number = self.__port_number
        )
        self.__log_file = 'datavolume/'+server_name+'-'+\
                          str(port_number)+'-log.txt'

        self.log('Bluetooth Device {0}:{1} Started'\
                 .format(server_name, port_number))

        self.log('Setting server_name to {0}'.format(server_name))
        self.set_value('server_name', server_name)
        self.log('Stored {0}'.format(self.get_value('server_name')))

        self.log('Setting port number to {0}'.format(port_number))
        self.set_value('port_number', port_number)
        self.log('Stored {0}'.format(self.get_value('port_number')))

        self.log('Setting Host IP Address to {0}'.format(host_ip))
        self.set_value('ip_addr', host_ip)
        self.log('Stored {0}'.format(self.get_value('ip_addr')))

        self.log('Setting version to {0}'.format(version))
        self.set_value('version', version)
        self.log('Stored {0}'.format(self.get_value('version')))


    def get_pairing_db(self):
        return self.__pairing_db

    def get_value(self, key=None):
        if key == None:
            return None

        return self.__pairing_db.get_key(key)


    def set_value(self, key=None, value=None):
        if key == None:
            return None

        return self.__pairing_db.set_key(key, value)


    def clear_value(self, key=None):
        if key == None:
            return None

        return self.__pairing_db.clear_key(key)


    def db_logger(self,
                  central_logger=None,
                  sender=None,
                  log_type=None,
                  log_message=None
    ):
        if central_logger == None:
            return
        try:
            payload_data = {
                "sender":sender,
                "log-type":"normal",
                "message":log_message
            }
            requests.post(
                central_logger,
                data=json.dumps(payload_data),
                timeout=10 # If nothing after 10s. ignore central
            ) # Ignore return from central logger
        except Exception as e:
            self.log(log_message='Exception: {0}'.format(repr(e)),
                log_to_central=False)
            print(repr(e))


    def log(self,
            log_message=None,
            log_to_central=True
    ):
        now = datetime.datetime.now()
        f = None
        try:
            sender = 'bluetooth_' + str(self.__port_number)
            central_logger = self.get_value('logger')
            if central_logger not in ('', [], None) \
            and log_to_central \
            and log_message != None:
                self.db_logger(central_logger, sender, 'normal', log_message)
            f = open(self.__log_file, 'a')
            if log_message == None or log_message == '':
                f.write("{0:>28s}\n".format(str(now)+': '))
            else:
                wrapped80 = wrap(log_message, 79)
                time_line = [str(now)]
                for line in wrapped80:
                    time_line.append('')
                for i, line in enumerate(wrapped80):
                    f.write('{0:>28s}{1}'.format(time_line[i]+': ', line)+"\n")
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

global_control = Control()
