from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone.Phone_Database import Phone_Database

import datetime, time, json, os, redis, requests
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

        self.log('Phone {0}:{1} Started'.format(server_name, port_number),
                 screen=False)


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


    def db_logger(self,
                  central_logger=None,
                  sender=None,
                  log_type=None,
                  log_message=None
    ):
        if central_logger == None:
            return
        try:
            sender = 'phone_' + str(self.__port_number)
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
            print(repr(e))


    def log(self,
            log_message=None,
            screen=True
    ):
        now = datetime.datetime.now()
        f = None
        try:
            central_logger = self.get_value('logger')
            if central_logger not in ('', [], None) and log_message != None:
                sender = 'phone_' + str(self.__port_number)
                self.db_logger(central_logger, sender, 'normal', log_message)
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
                if screen:
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


    def handle_unlock(self):
        self.log('Device has been unlocked. Handle any persisted '+\
                 'notifications stored in local store.',
                 screen=False)
        notifications_persisted = self.__phone_db.get_notifications()
        for note in notifications_persisted:
            self.process_notification(
                sender=note[0],
                date_string=note[1],
                notification=note[2],
                action=note[3]
            )
            self.log('Showing {0}'.format(note[0]),
                     screen=False)


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


    def process_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        self.log(
            'Displaying notification on screen',
            screen=False
        )

        self.display_notification(
            sender=sender,
            date_string=date_string,
            notification=notification,
            action=action
        )

        self.__phone_db.update_notification(
            sender=sender,
            date_string=date_string,
            notification=notification,
            action=action
        )

        self.log(
            'Issuing notification to Bluetooth devices',
            screen=False
        )

        self.issue_bluetooth(notification=notification)


    def issue_bluetooth(
        self,
        notification=None
    ):
        request_response = None

        try:
            bluetooth_device = self.get_bluetooth()
            if bluetooth_device != []\
            and bluetooth_device != None:
                bluetooth_key = self.get_value(bluetooth_device)
                phonename = self.get_value('phonename')
                if not (bluetooth_key == None or phonename == None):
                    payload_data = {
                                    "key":bluetooth_key,
                                    "message":notification
                                   }
                    request_response = requests.post(
                         bluetooth_device+'/broadcast/'+phonename,
                         data=json.dumps(payload_data)
                    )
            return request_response
        except requests.exceptions.ConnectionError as rce:
            self.log(
                'Bluetooth caused an exception: {0}'.format(rce),
                screen=False
            )
#            raise requests.exceptions.ConnectionError(rce)
        except:
            raise

    def display_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        try:
            self.log('')
            self.log('Notification received')
            self.log('-'*79)
            self.log('Notification from: {0}'.format(sender))
            self.log('Received at      : {0}'.format(date_string))
            self.log('Notification     : {0}'.format(notification))
            self.log('Action           : {0}'.format(action))
            self.log('')

            outputfile = self.get_value('output_device')
            f = open(outputfile,'a')
            f.write(('-'*80)+"\n")
            f.write('Notification from: {0}'.format(sender)+"\n")
            f.write('Received at      : {0}'.format(date_string)+"\n")
            f.write('Notification     : {0}'.format(notification)+"\n")
            f.write('Action           : {0}'.format(action)+"\n\n")
            f.close()
        except:
            raise


global_controller = Control()

