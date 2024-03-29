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
from Links import Link_Schema, Link_Collection, Link
from Methods import Methods
from Server import Server

# Import Marshmallow for schema loading #
from marshmallow import Schema, fields, post_load

# Import jsonschema validator
from jsonschema import validate

# Import CMD
from cmd2 import Cmd

# Global variables
interactive = False
server = None
g_links = Link_Collection()

# Class definition for cmd2
class App(Cmd):

    def do_print(self, line):
        print ('{0}'.format(line))

    def do_server(self, line):
        global server
        server = Server(line)
        self.prompt = str(server)+' >> '

    def do_close(self, line):
        global server
        global g_links
        server = None
        g_links = Link_Collection()
        self.prompt = str(server)+' >> '

    def do_get(self, line):
        do_command('GET', line)

    def do_put(self, line):
        do_command('PUT', line)

    def do_post(self, line):
        do_command('POST', line)

    def do_delete(self, line):
        do_command('DELETE', line)

    def do_options(self, line):
        do_command('OPTIONS', line)

    def do_head(self, line):
        do_command('HEAD', line)

    def do_test(self, line):
        do_command(1, 1)

    def do_routes(self, line):
        get_routes(line)

def __print_output(data_set=None, headers=None):
    for header_item in headers:
        print('{0:20s} {1}'.format(header_item, headers[header_item]))
    print()
    pprint(data_set)

def get_routes(command):
    try:
        global server
        global g_links

        args = command.split()
        verbose = False
        if len(args) > 0:
            if args[0] == '--verbose':
                verbose = True
                print('Set verbose')
            else:
                raise Exception('correct usage: routes <--verbose>, '+\
                                 'where <--verbose> displays full details.')

        if server == None:
            raise Exception('Server must be set using: server <servername>')

        g_links.get_links(server.server_name)

        print()
        for link in g_links.links:
            print(link.identifier, link.description)
            print('{0}'.format('-'*80))
            print('URL:       ', link.href)
            print('Methods:   ', str(link.methods))
            print('Schema:    ', str(link.schema))
            print('Parameters:',str(link.parameters))
            print()
            print()

    except ValueError as e:
        print('{0} {1}'.format(e, server.server_name))
    except Exception as e:
        print('error. '+str(e))

def do_command(method, command):
    if not type(method) == str \
    and not type(command) == str:
        raise Exception('{0} {1} is invalid!'.format(method, command))

    if not method.upper() in ['GET','PUT','POST','DELETE','OPTIONS','HEAD']:
        raise Exception('{0} is an invalid method!'.format(method))

    args = command.split()
    if len(args) < 1:
        raise Exception('correct usage: get <route>, where <route> '+\
                        'is a number.')
    if g_links == []:
        raise Exception('The routes command must be executed before {0}'\
                        .format(method))
    command = int(command)

    try:
        validated_state = False
        route = int(command)

        if route < 0:
            raise ValueError("The route cannot be less than zero.")
        elif len(g_links.links) < 1:
            raise IndexError("There are no routes. The commands "+\
                             "server <http://server> and routes "+\
                             "must be executed before {0}"\
                             .format(method))
        elif route >= len(g_links.links):
            raise IndexError("The route doesn't appear to exist. ")
        if not method in g_links.links[route].methods:
            raise Exception('HTTP 405 - This route does not support {0}'\
                            .format(method))

        methods = Methods()
        if method.upper() == 'GET':
            data_set, headers = methods.get(g_links, command)
        elif method.upper() == 'PUT':
            data_set, headers = methods.put(g_links, command)
        elif method.upper() == 'POST':
            data_set, headers = methods.post(g_links, command)
        elif method.upper() == 'DELETE':
            data_set, headers = methods.delete(g_links, command)
        elif method.upper() == 'OPTIONS':
            data_set, headers = methods.options(g_links, command)
        elif method.upper() == 'HEAD':
            data_set, headers = methods.head(g_links, command)
        else:
            raise Exception('Sorry, {0} is not currently supported.'\
                            .format(method))

        __print_output(data_set, headers)
    except Exception as e:
        print('error. '+str(e))

def help(server):
    print()
    print('options')
    print()
    print('help - execute this command')
    print('routes - list all routes available from root server {0}' \
          .format(server.server_name))
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
    App.prompt = ' >> '
    App.intro = 'Command line microservice interpreter. Remember to '+\
                    'set the server using: server <servername>'

    App().cmdloop()
