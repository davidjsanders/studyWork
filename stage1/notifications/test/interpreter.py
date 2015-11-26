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

# Import Marshmallow for schema loading #
from marshmallow import Schema, fields, post_load

# Import jsonschema validator
from jsonschema import validate

# Import CMD
from cmd2 import Cmd

# Class definitions
class Server(object):
    def __init__(
        self,
        server_name='http://localhost:5000/v1_00/'
    ):
        self.server_name = server_name

    def __repr__(self):
        return self.server_name

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
        server = None
        self.prompt = str(server)+' >> '

    def do_get(self, line):
        get(line)

    def do_head(self, line):
        header(line)

    def do_routes(self, line):
        fetch_routes(line)

def fetch_routes(command):
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
            print('Parameters:',str(link.parameters))
            print()
            print()

    except ValueError as e:
        print('{0} {1}'.format(e, server.server_name))
    except Exception as e:
        print('error. '+str(e))

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

        methods = Methods()
        data_set, headers = methods.get(g_links, command)
        for header_item in headers:
            print('{0:20s} {1}'.format(header_item, headers[header_item]))
        print()
        pprint(data_set)

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