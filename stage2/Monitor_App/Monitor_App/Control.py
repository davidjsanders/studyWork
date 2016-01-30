from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App.Monitor_App_Database \
    import Monitor_App_Database

import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = 'datavolume/Log_File.txt'
    __Monitor_App_db = None

    def __init__(self):
        self.__Monitor_App_db = Monitor_App_Database()


    def get_state(self):
        return self.__Monitor_App_db.get_state()


    def set_state(self, state=None):
        return self.__Monitor_App_db.set_state(state)


    def set_value(self, key=None, value=None):
        return self.__Monitor_App_db.set_value(key, value)


    def get_value(self, key=None):
        return self.__Monitor_App_db.get_value(key)


    def clear_value(self, key=None):
        return self.set_value(key, None)


    def check_location(self):
        state = self.get_state()
        if state.upper() == 'ON':
            print('Checking location for hot spot!')

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


    def write_console(self, message=None):
        if message == None:
            return

        print(message)


    def print_error(self, error_message=None):
        print('{0}'.format('-'*80))
        print('*** {0} ***'.format(error_message))
        print('{0}'.format('-'*80))
#
# Version 1.00
# ----------------------------------------------------------------------------
class Control_v1_00(Control):
    def future(self):
        pass

