#!/usr/bin/python3
import requests, argparse
from textwrap import wrap

class v3_00_Show_Log(object):
    output_mode = 'print'
    print_underline = '\033[4m'
    print_bold = '\033[1m'
    print_normal = '\033[0m'

    print_header_1 = print_underline +\
                     print_bold +\
                     '{0:<132s}' +\
                     print_normal

    print_header_2 = print_underline +\
                     '{0:<132s}' +\
                     print_normal

    print_all_line = '{0:<21s}|{1:<10s}|{2:<20s}|{3:<78s}'
    print_one_line = '{0:<23s}|{1:<10s}|{3:<97s}'

    module_description = 'Connect to the logging service and show the logs. '+\
                         'The logs from each Docker machine running a '+\
                         'component of the model are available either as '+\
                         'a whole or individually. When viewed as a whole, '+\
                          'the log report shows every machine; when viewed '+\
                          'for a single machine, only that machines log is '+\
                         'shown. The log will be large and can be piped to '+\
                          'more or out to a file.'
    logger_description = 'The URL identifier for the logging server, '+\
                         'If only the log URL is provide, e.g.: '+\
                         'http://server:port/v9_99/log, then the logs for '+\
                         'all devices will be shown. If only the logs for a '+\
                         'specific machine are required, then you should '+\
                         'pass the full URL, e.g. '+\
                         'http://srvr:port/v9/log/docker_name, to '+\
                         'display only the logs for that machine. '+\
                         'Note: do NOT add trailing / characters to any URL.'
    server_description = 'The service name of the server. Please '+\
                         'note; this is simply the server name '+\
                         '(e.g. bob_321) not the FQDN or http://server. '+\
                         'The server name is used in the logging tables '+\
                         'as the unique key.'


    def output_error(self, text=' '):
        self.output_line(self.print_header_1.format('An error occurred '+\
                            'while connecting to the log server.')
        )
        self.output_line(text)


    def output_line(self, text=''):
        if self.output_mode == 'print':
            self.print_line(text)
#
# For future use, e.g. adding file output
#
#        else:
#            self.print_line(text)


    def print_line(self, text=''):
        print("{0}".format(text))


    def print_log(self, log=None, log_all=True):
        if log == None:
            return
    
        if log_all:
            line_to_print = self.print_all_line
        else:
            line_to_print = self.print_one_line

        self.output_line(self.print_underline +\
                         self.print_bold +\
                         line_to_print\
                             .format('Time','Type','Sender','Log Message')+\
                         self.print_normal
        )

        for row in log:
            sender = row['sender']
            timestamp = row['timestamp']
            log_type = row['log-type']
            message = row['message']
            wrapped_message = wrap(message, 78)
            loop = 0
            while loop < len(wrapped_message):
                self.output_line(line_to_print\
                  .format(timestamp[:21] if loop == 0 else ' ',
                          log_type[:10] if loop == 0 else ' ',
                          sender[:20] if loop == 0 else ' ',
                          wrapped_message[loop]))
                loop += 1


    def __init__(self):
        self.output_mode = 'print'
        self.column_width = 132

        try:
            parser = argparse.ArgumentParser(
                description=self.module_description
            )
            parser.add_argument('--logger',
                                type=str,
                                help=self.logger_description,
                                required=True)
            parser.add_argument('--server',
                                type=str,
                                help=self.server_description,
                                required=False)

            args = parser.parse_args()

            if args.server == None:
                server_name = 'all'
                server_info = None
            else:
                server_name = args.server
                server_info = '/'+str(server_name)

            log_service = args.logger
            if server_info != None:
                log_service += server_info

            self.output_line(self.print_header_1.format('Logs'))
            self.output_line('Service: {0}'\
                  .format(server_info[1:] \
                          if server_info != None else '** All **'
                  )
            )
            self.output_line('Logger : {0}'.format(args.logger))
            self.output_line('Request: curl -X GET {0}'.format(log_service))
            self.output_line()

            r = requests.get(log_service)
            if r.status_code not in (200, 201):
                raise requests.exceptions.HTTPError(str(r.status_code)+': '+r.text)

            json_data = r.json()
            if json_data['data']['log'] == None:
                raise KeyError(server_info)

            if len(json_data['data']['log']) == 0:
                raise ValueError('There is no data in the log to show.')

            self.output_line(self.print_header_1.format('Header Response'))
            for header in r.headers:
                self.output_line('{0:20}:{1}'.format(header, r.headers[header]))
            self.output_line()
            self.output_line('{0:20}:{1}'.format('status code', r.status_code))
            self.output_line()

            self.output_line(self.print_header_1.format('Start of logs'))
            self.output_line()

            if server_info == None:
                log_all = True
            else:
                log_all = False
            self.print_log(log=json_data['data']['log'], log_all=log_all)

        except requests.exceptions.ConnectionError as rce:
            self.output_error('Unable to connect to {0}. Error {1}'\
                              .format(args.logger, rce) + '. ' +\
                              'Are you sure the logger is running and the '+\
                              'URL is correct?'
            )
        except requests.exceptions.HTTPError as he:
            self.output_error(str(he))
            self.output_line()
            self.output_line('The log server may be busy. Please try again '+\
                             'shortly.')
        except ValueError as ve:
            self.output_line(str(ve))
        except Exception as e:
            self.output_error(repr(e))
        finally:
            self.output_line()
            self.output_line(self.print_header_1.format(' '))
            self.output_line('*** End of logs ***')
            self.output_line()

