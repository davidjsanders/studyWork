#!/usr/bin/python3
import requests, argparse
from textwrap import wrap

def print_log(log=None):
    if log == None:
        return

    print('\033[1m\033[4m{0:<20s}|{1:<21s}|{2:<10s}|{3:<78s}\033[0m'\
          .format('Sender','Time','Type','Log Message'))

#    print('='*column_width)
    for row in log:
        wrapped_message = wrap(row[3], 78)
        loop = 0
        while loop < len(wrapped_message):
            if loop == 0:
                print('{0:<20s}|{1:<21s}|{2:<10s}|{3:<78s}'\
                      .format(row[0][:20],
                              row[1][:21],
                              row[2][:10],
                              wrapped_message[loop]))
            else:
                print('{0:<20s}|{1:<21s}|{2:<10s}|{3:<78s}'\
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
#    print('='*column_width)
    for row in log:
        wrapped_message = wrap(row[3], 97)
        loop = 0
        while loop < len(wrapped_message):
            if loop == 0:
                print('{0:<23s}|{1:<10s}|{2:<97s}'\
                      .format(row[1][:23], row[2][:10], wrapped_message[loop]))
            else:
                print('{0:<23s}|{1:<10s}|{2:<97s}'\
                      .format(' ', ' ', wrapped_message[loop]))
            loop += 1


column_width = 132
try:
    parser = argparse.ArgumentParser(description='Show log for server and port')
    parser.add_argument('--server',
                        type=str,
                        help='The name or IP address of the server. Please '+\
                             'note; this is simply the server name '+\
                             '(e.g. bob) and not the FQDN or http://server. '+\
                             'The server name is used in the logging tables '+\
                             'with the port number as the unique key.',
                        required=False)
    parser.add_argument('--port',
                        type=int,
                        help='The port number (e.g. 80) used by the server. '+\
                             'Please note; this is simply the port '+\
                             '(e.g. 8090). '+\
                             'The port name is used in the logging tables '+\
                             'with the server name as the unique key.',
                        required=False)
    parser.add_argument('--logger',
                        type=str,
                        help='The URL identifier for the logging server, '+\
                             'which must be provided as a fully qualified '+\
                             'domain name AND with the correct path to the '+\
                             'logging service; e.g. '+\
                             'http://bob:8080/v1_00/log   --- NOTE: there is '+\
                             'no trailing / character.'
                             ,
                        required=True)
    args = parser.parse_args()
    if args.server == None:
        server_name = 'all'
        port_number = 0
        server_info = None
    else:
        server_name = args.server
        if args.port == None:
            raise ValueError('If the server is specified, the port number '+\
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

