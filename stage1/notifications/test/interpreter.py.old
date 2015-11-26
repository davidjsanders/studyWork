#!/usr/bin/python3
# Import 
# Reference: 
# Argparse Tutorial - https://docs.python.org/2/howto/argparse.html#id1
#
# Import argpars to parse command line arguments
import argparse

# Import text wrapping module
import textwrap

# Import requests, sys, json, and pprint for http methods and formatting #
import requests
import sys
import json
from pprint import pprint

# Import Marshmallow for schema loading #
from marshmallow import Schema, fields, post_load

# Import jsonschema validator
from jsonschema import validate

# Global variables
interactive = False
server = ''
g_links = []

# Import CMD
from cmd2 import Cmd

# Load links schema
f = open('schemas/links.json','r')
__schema__ = json.load(f)
f.close()

# Class definitions
class Link(object):
    def __init__(self,
                 description=None,
                 href=None,
                 rel=None,
                 methods=[],
                 identifier=-1):
        self.headers = []
        self.name = ''
        self.identifier = identifier
        self.description = description
        self.href = href
        self.rel = rel
        self.parameters = []
        self.methods = methods

    def __repr__(self):
        return '<Link(identifier={self.identifier!r}>'.format(self=self)

    def to_string(self):
        return str(self.identifier) + ' ' + \
               self.description + ' (' + \
               self.href + ') ' + \
               str(self.methods)

    def get_headers(self):
        return
        result = requests.options(self.href)
        if result.status_code == 200:
            self.headers = result.headers

# Schema definition for Marshmallow
class LinkSchema(Schema):
    description = fields.Str(required=True)
    identifier = fields.Int(required=True)
    href = fields.Str(required=False)
    rel = fields.Str(required=True)
    methods = fields.List(fields.Str())

    @post_load
    def make_link(self, data):
        return Link(**data)

# Class definition for cmd2
class App(Cmd):

    def do_print(self, line):
        '''
print [args]: print to standard out
===================================
Print a small message to standard output. All text after print will be printed 
and redirection is honored
'''
        print ('{0}'.format(line))

    def do_server(self, line):
        '''
server [arg]: connect to server
===============================
Connect to a service running on a fully qualified URL [arg], e.g. 
http://<host>:<port>/url). Note, the URL must be fully qualified and 
the program expects a service at the endpoint; if not, errors will be reported.
'''
        global server
        server = line
        self.prompt = server+' >> '

    def do_close(self, line):
        '''
close: close current server
===========================
Closes the currently open server and returns control to the user.
'''
        global server
        server = ''
        self.prompt = server+' >> '

    def do_get(self, line):
        '''
get [arg] [arg2]: execute a get statement from known routes
===========================================================
Connect to the current service and execute one of the known routes (known from
issuing a 'routes' command (see help routes). The first argument is the route
id. If a second argument is present, get will look for a dictionary key with
the value of arg2. Typically get <route> is executed first, then the user
executes get <route> <key> from the list of keys returned.
'''
        get(line)

    def do_head(self, line):
        '''
head [arg]: get the OPTIONS for a known route
=============================================
Connect to the current service and execute an options (curl -X OPTIONS...) 
on a known route given as an argument. The route is known from issuing a 
'routes' command (see help routes). The first argument is the route id.
The head command typically shows the date, content-type, server, connection,
allow, and content-length fields. The allow is particularly important as it
defines the type of HTTP requests (GET, PUT, POST, DELETE, HEAD, OPTIONS, etc.)
which are permitted for the route.
'''
        header(line)

    def do_routes(self, line):
        '''
routes [--verbose]: get a list of routes (known routes) from the server
=======================================================================
Connect to the current service and tell it to return the list of routes
available from the service. If the flag --verbose is used, then the full set
of information (id, description, url, and methods) are shown.

Once the list of known routes has been created, other commands (e.g. put, get,
etc.) can be executed by typing: get <route id> (see help get).
'''
        fetch_routes(line)

def fetch_routes(command):
    '''
    This is the help text :)
    '''
    try:
        global server
        args = command.split()
        verbose = False
        if len(args) > 0:
            if args[0] == '--verbose':
                verbose = True
                print('Set verbose')
            else:
                raise Exception('correct usage: routes <--verbose>, '+\
                                 'where <--verbose> displays full details.')

        global g_links
        g_links = []

        result = requests.get(server)
        if not result.status_code == 200\
        or 'error' in result.json():
            raise Exception('The server issued a bad response.')

        if '_links' in result.json()['success']['data']:
            _links = result.json()['success']['data']['_links']
            # Define a sort function for the links list of objects
            # Reference -
            # http://pythoncentral.io/
            #   how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
            def getKey(item):
                return _links[item]['identifier']

            counter = 0
            print()
#            print_route_header(verbose)
            for link in sorted(_links, key=getKey):
                validate(_links[link], __schema__)
                _link = LinkSchema(strict=True).load(_links[link]).data
#                _link.identifier = counter
#                _link.get_headers()
                _link.name = link
                counter += 1
                g_links.append(_link)
                print(_link.to_string())
#                print_route(_link, verbose)
#            print_route_footer(verbose)
        else:
            raise ValueError('No links were found at the root address:')
    except ValueError as e:
        print('{0} {1}'.format(e, server))
    except Exception as e:
        print('error. '+str(e))

def print_route_header(verbosity):
    if verbosity:
        pass
    else:
        print('\033[4m{0:3s} {1:20s} {2:28s} {3:25s}\033[0m'.format(
              ' ID', 'Route Name', 'Description', 'Methods Allowed'
        ))
#        print('{0}'.format('='*80))

def print_route_footer(verbosity):
    print()

def print_route(link, verbosity):
    if verbosity:
        pass
    else:
        print_route_table(link, verbosity)

def print_route_table(link, verbosity):
    name = textwrap.wrap(link.name, width=20)
    description = textwrap.wrap(link.description, width=28)
#    href = textwrap.wrap(link.href, width=25)
    href = []
    allow = textwrap.wrap(link.headers['allow'], width = 25)

    sizes = [len(name), len(description), len(href), len(allow)]
    max_size = max(sizes)
    underline_counter = max_size - 1

    counter = 0
    while True:
        if counter == max_size:
            break

        name_print = ''
        description_print = ''
        href_print = ''
        allow_print = ''
        if counter == 0:
            identifier = str(link.identifier).rjust(3, ' ')
        else:
            identifier = ''

        try:
            if counter < len(name):
                name_print = name[counter]
            if counter < len(description):
                description_print = description[counter]
            if counter < len(href):
                href_print = href[counter]
            if counter < len(allow):
                allow_print = allow[counter]
            print('{0:3s} {1:20s} {2:28s} {3:25s}'.format(
                identifier
               ,name_print
               ,description_print
               ,allow_print
            ))
        except Exception as e:
            print('error: '+repr(e))
        counter += 1

#    print('{0}'.format('-'*80))

    return

def fetch_route(command):
    try:
        args = command.split()
        if len(args) < 2:
            raise ValueError('correct usage: route <route>, where <route> '+\
                             'is a number.')
    except ValueError as e:
        print(e)
    except Exception as e:
        print('error. '+str(e))

def header(command):
    try:
        args = command.split()
        if len(args) < 1 or len(args) > 1:
            raise Exception('correct usage: '+args[0]+' <route>, where <route> '+\
                             'is a number.')

        route = int(args[0])
        if route < 0:
            raise ValueError("The route cannot be less than zero.")
        elif route > len(g_links):
            raise IndexError("The route doesn't exist. Have you run routes?")

        print()
        headers = g_links[route].headers
        for header_item in headers:
            print('{0:20s} {1}'.format(header_item, headers[header_item]))
        print()
    except Exception as e:
        print('error. '+str(e))

def get(command):
    try:
        args = command.split()
        if len(args) < 1:
            raise Exception('correct usage: get <route>, where <route> '+\
                             'is a number.')

        content_to_find = None
        if len(args) > 1:
            content_to_find = str(args[1])

        route = int(args[0])
        if route < 0:
            raise ValueError("The route cannot be less than zero.")
        elif route > len(g_links):
            raise IndexError("The route doesn't exist. Have you run routes?")
        if not 'GET' in g_links[route].headers['allow']:
            raise Exception('HTTP 405 - This route does not support GET')

        result = requests.get(g_links[route].href)
        if not result.status_code == 200:
            raise Exception('HTTP {0}'.format(result.status_code))
        elif not 'json' in result.headers['content-type']:
            raise Exception('Expected JSON data but did not receive it.')

        print()
        headers = result.headers
        for header_item in headers:
            print('{0:20s} {1}'.format(header_item, headers[header_item]))
        print()

        data_set = result.json()
        data_keys = data_set.keys()

        if not content_to_find == None:
            if not content_to_find in data_set:
                key_string = ""
                for key in data_set.keys():
                    key_string = key_string + key + ','
                raise Exception('Content "'+content_to_find+ \
                                '" does not exist. Possible choices are '+ \
                                'one of: [' + \
                                key_string + ']')
            if type(data_set[content_to_find]) is dict:
                print('Data')
                print('-'*80)
                for key in data_set[content_to_find]:
                    if key != '_links':
                        print('{0:30s}: {1}' \
                              .format(key, data_set[content_to_find][key]))
                print()
                print('Links')
                print('-'*80)
                for key in data_set[content_to_find]['_links']:
                    print('{0:30s}: {1}'.format(key, data_set[content_to_find]['_links'][key]))
            else:
                pprint(data_set)
        else:
            print('Keys')
            print('-'*80)
            for key in data_keys:
               print('{0}'.format(key))
        print()

    except Exception as e:
        print('error. '+str(e))

def help(server):
    print()
    print('options')
    print()
    print('help - execute this command')
    print('routes - list all routes available from root server {0}' \
          .format(server))
    print('get <route> - get (curl -X GET) the route identified '+ \
          'by <route> returning keys in dictionary items, otherwise ' +\
          'the values.')
    print('get <route> <key> - get (curl -X GET) the route identified '+\
          'by <route> and <key>')
    print('put <route> <key> - put (curl -X PUT) the route identified by <route>')
    print('post <route> - post (curl -X POST) the route identified by <route>')
    print('delete <route> - post (curl -X DELETE) the route '+\
          'identified by <route>')
    print('head <route> - show the header and options for <route>')
    print()

if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.add_argument("server"
#                       ,type=str
#                       ,help="Fully qualified url for the device"+\
#                             ", e.g. http://localhost:82/ **NOTE** "+\
#                             "the port and closing / should be provided")
#    args = parser.parse_args()
#    if args.server:
#        global server
#        server = args.server
    App.prompt = ' >> '
    App.intro = 'Command line microservice interpreter. Remember to '+\
                    'set the server using: server <servername>'

    App().cmdloop()
