#!/usr/bin/python3
import requests, argparse
from textwrap import wrap

def print_log(log=None):
    if log == None:
        return

    print('\033[1m\033[4m{1:<21s}|{2:<10s}|{0:<20s}|{3:<78s}\033[0m'\
          .format('Sender','Time','Type','Log Message'))

    for row in log:
        sender = row['sender']
        timestamp = row['timestamp']
        log_type = row['log-type']
        message = row['message']
        wrapped_message = wrap(message, 78)
        loop = 0
        while loop < len(wrapped_message):
            if loop == 0:
                print('{0:<21s}|{1:<10s}|{2:<20s}|{3:<78s}'\
                      .format(timestamp[:21],
                              log_type[:10],
                              sender[:20],
                              wrapped_message[loop]))
            else:
                print('{0:<21s}|{1:<10s}|{2:<20s}|{3:<78s}'\
                      .format(' ',
                              ' ',
                              ' ',
                              wrapped_message[loop]))
            loop += 1


def print_single_log(log=None):
    if log == None:
        return

    print('\033[1m\033[4m{0:<23s}|{1:<10s}|{2:<97s}\033[0m'\
          .format('Time','Type','Log Message'))

    for row in log:
        sender = row['sender']
        timestamp = row['timestamp']
        log_type = row['log-type']
        message = row['message']
        wrapped_message = wrap(message, 97)
        loop = 0
        while loop < len(wrapped_message):
            if loop == 0:
                print('{0:<23s}|{1:<10s}|{2:<97s}'\
                      .format(timestamp[:23], log_type[:10], wrapped_message[loop]))
            else:
                print('{0:<23s}|{1:<10s}|{2:<97s}'\
                      .format(' ', ' ', wrapped_message[loop]))
            loop += 1


column_width = 132
try:
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
    parser = argparse.ArgumentParser(description=module_description)
    parser.add_argument('--logger',
                        type=str,
                        help=logger_description,
                        required=True)
    parser.add_argument('--service',
                        type=str,
                        help='The name of the service. Please '+\
                             'note; this is simply the service name '+\
                             '(e.g. phone or loc_svc) and not the '+\
                             'URL, FQDN or http://server address. '+\
                             'The service name is used in the logging tables '+\
                             'with the port number as the unique key.',
                        required=False)
    parser.add_argument('--port',
                        type=int,
                        help='The port number used by the service. '+\
                             'Please note; this is simply the port '+\
                             '(e.g. 55000). '+\
                             'The port name is used in the logging tables '+\
                             'with the server name as the unique key.',
                        required=False)
    args = parser.parse_args()
    if args.service == None:
        server_name = 'all'
        port_number = 0
        server_info = None
    else:
        server_name = args.service
        if args.port == None:
            raise ValueError('If the service is specified, the port number '+\
                             'must be provided too!')
        else:
            server_info = '/'+str(server_name)+'_'+str(args.port)

    log_service = args.logger
    if server_info != None:
        log_service += server_info

    print('\033[2J\033[1;1H')
    print('\033[1m\033[4m{0:<132s}\033[0m'.format('Logs'))
    print('Service: {0}'\
          .format(server_info[1:] if server_info != None else '** All **'))
    print('Logger : {0}'.format(args.logger))
    print('Request: curl -X GET {0}'.format(log_service))
    print()

    r = requests.get(log_service)
    if r.status_code not in (200, 201):
        raise requests.exceptions.HTTPError(str(r.status_code)+': '+r.text)

    json_data = r.json()
    if json_data['data']['log'] == None:
        raise KeyError(server_info)

    print('\033[1m\033[4m{0:<132s}\033[0m'.format('Header Response'))
    for header in r.headers:
        print('{0:20}:{1}'.format(header, r.headers[header]))
    print()
    print('{0:20}:{1}'.format('status code', r.status_code))
    print()

    print('\033[1m\033[4m{0:<132s}\033[0m'.format('Start of logs'))
    print()

    if server_info == None:
        print_log(log=json_data['data']['log'])
    else:
        print_single_log(log=json_data['data']['log'])

    print()
    print('\033[1m\033[4m{0:<132s}\033[0m'.format('End of logs'))
except requests.exceptions.ConnectionError as rce:
    print('Unable to connect to {0}. Error {1}'.format(args.logger, rce))
except requests.exceptions.HTTPError as he:
    print('Unable to process logs. Error {0}'.format(he))
except ValueError as ve:
    print(str(ve))
except KeyError as ke:
    print('Error 404: There is no log information for {0}'.format(ke))
except Exception as e:
    print(repr(e))
finally:
    print()

