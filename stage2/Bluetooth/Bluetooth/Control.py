from flask import Response
from Bluetooth import PairingDatabase

import datetime, time, json

class Control(object):
    __pairing_db = None
    __config_database = 'datavolume/config.db'
    __broadcast_filename = 'datavolume/broadcasted_output.txt'
    __display_filename = 'datavolume/display_output.txt'

    def __init__(self):
        self.__pairing_db = PairingDatabase.Pairing_Database()

    def broadcast_message(self, devicename='Unknown', text=None, key=None):
        success = 'success'
        status = '201'
        message = 'Message has been broadcast.'
        data = {"device":devicename,
                "action":"broadcast",
                "message":text}

        pairing_key = self.__pairing_db.check_pairing(devicename)
        if pairing_key == []:
            success = 'error'
            status = '403'
            message = 'Device is not paired'
            pairing_key = None
        elif pairing_key != key:
            success = 'error'
            status = '403'
            message = 'Device pairing key is incorrect!'
            pairing_key = None
        elif text == '' or text == None:
            success = 'error'
            status = '403'
            message = 'Cannot broadcast an empty message'
            pairing_key = None
        else:
            try:
                now = datetime.datetime.now()
                tz = time.tzname[0]
                tzdst = time.tzname[1]

                f = open(self.__broadcast_filename,'a')
                f.write(('-'*80)+"\n")
                f.write('Broadcast from: {0}'.format(devicename)+"\n")
                f.write('Read aloud at: {0} ({1}/{2})'\
                    .format(now, tz, tzdst)+"\n")
                f.write('Message: {0}'.format(text)+"\n\n")
                f.close()

                f = open(self.__display_filename,'a')
                f.write(('-'*80)+"\n")
                f.write('Broadcast from: {0}'.format(devicename)+"\n")
                f.write('Shown on screen at: {0} ({1}/{2})'\
                    .format(now, tz, tzdst)+"\n")
                f.write('Message: {0}'.format(text)+"\n\n")
                f.close()
            except:
                raise

        return self.do_response(message=message,
                                data=data,
                                status=status,
                                response=success)

    def pair_info(self, devicename):
        success = 'success'
        status = '201'
        message = 'Device is paired.'
        pairing = self.__pairing_db.check_pairing(devicename)

        if pairing == []:
            success = 'error'
            status = '404'
            message = 'Device is not paired'
            pairing = None

        data = {"device":devicename,
                "key":pairing}

        return self.do_response(message=message,
                                data=data,
                                status=status,
                                response=success)

    def pair_device(self, devicename):
        success = 'success'
        status = '201'
        message = 'Device successfully paired.'
        existing_key = self.__pairing_db.check_pairing(devicename) or None

        if existing_key != None:
            success = 'error'
            status = '409'
            message = 'The device is already paired.'
            data = {"device":devicename,
                    "key":existing_key}
        else:
            data = {"device":devicename,
                    "key":self.__pairing_db.pair_device(devicename)}
        return self.do_response(message=message,
                                data=data,
                                status=status,
                                response=success)

    def pair_unpair(self, devicename):
        if not self.__pairing_db.check_pairing(devicename):
            return self.do_response(status="404",
                                    response='error',
                                    message="{0} is not paired."\
                                        .format(devicename))
        if self.__pairing_db.remove_pairing(devicename):
            return self.do_response(message="{0} un-paired.".format(devicename))


    def do_response(self,
                    status=200,
                    response='success',
                    data=None,
                    message=''):
        return_dict = {"status":status,
                       "type":response,
                       "data":data,
                       "message":message}
        return Response(
            json.dumps(return_dict),
            status=status,
            mimetype='application/json')

