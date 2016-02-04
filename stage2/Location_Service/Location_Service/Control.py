from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Location_Service.Location_Service_Database \
    import Location_Service_Database

import datetime, time, json, os
from textwrap import wrap

class Control(object):
    __log_file = None
    __location_service_db = None

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

        self.__location_service_db = \
            Location_Service_Database(server_name, port_number)
        self.__log_file = 'datavolume/'+server_name+'-'+str(port_number)+\
            '-log.txt'
        self.log()
        self.log('*'*78)
        self.log('Location Service {0}:{1} Started'\
            .format(server_name, port_number))
        self.log('*'*78)
        self.log()

    def get_hotspots(self):
        return self.__location_service_db.get_hotspots()


    def get_hotspots_by_location(self, x, y):
        return self.__location_service_db.get_hotspot_by_location(x, y)


    def get_hotspot(self, location):
        return self.__location_service_db.get_hotspot_by_name(location)


    def save_hotspot(self, location, upperX, upperY, lowerX, lowerY, desc):
        return self.__location_service_db.set_hotspot(
            location,
            upperX,
            upperY,
            lowerX,
            lowerY,
            desc
        )


    def delete_hotspot(self, location):
        return self.__location_service_db.clear_hotspot(location)


    def log(self,
            log_message=None,
            screen=True
    ):
        now = datetime.datetime.now()
        f = None
        try:
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


    def write_console(self, message=None):
        if message == None:
            return

        print(message)


    def print_error(self, error_message=None):
        print('{0}'.format('-'*80))
        print('*** {0} ***'.format(error_message))
        print('{0}'.format('-'*80))

global_control = Control()
