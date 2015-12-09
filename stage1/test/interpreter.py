#!/usr/bin/python3
# Imports
# -------
# Import CMD - provides command line interface
from cmd2 import Cmd

# Import pprint for formatting #
from pprint import pprint

# Import Interpreter modules
from Links import Link_Collection
from Server import Server
from Utilities import Utilities
from Routes import get_routes

# Global variables
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
        '''
get
===
A command that issues a get request against a given route. Any parameters or
data required will be prompted for.
        '''
        do_command('GET', line)

    def do_put(self, line):
        '''
put
===
A command that issues a put request against a given route. Any parameters or
data required will be prompted for.
        '''
        do_command('PUT', line)

    def do_post(self, line):
        '''
post
====
A command that issues a post request against a given route. Any parameters or
data required will be prompted for.
        '''
        do_command('POST', line)

    def do_delete(self, line):
        '''
put
===
A command that issues a delete request against a given route. Any parameters or
data required will be prompted for.

!! CAUTION !!
=============
Delete does NOT prompt.
        '''
        do_command('DELETE', line)

    def do_options(self, line):
        '''
options
=======
A command that issues an options request against a given route and displays the
allowed methods (e.g. GET, PUT, etc.) for the route.
        '''
        do_command('OPTIONS', line)

    def do_head(self, line):
        '''
put
===
A command that issues a head request against a given route and displays the
header for the route.
        '''
        do_command('HEAD', line)

    def do_test(self, line):
        '''
put
===
A test command to cause failure on do_command.
        '''
        do_command('TEST', line)

    def do_routes(self, line):
        '''
routes
======
A command that issues a get request to the web services root and expects to 
receive a stream of JSON data in return which confirms to a known schema 
(links.json).

Issuing the command 'routes' calls the web service, retrieves the JSON data,
validates the data against the schema and then presents the list of routes
indexed by a number. Commands can then be executed against a route by entering
the method and the route number; e.g. get 2, will issue an HTTP GET request
against the 2nd route listed, while post 2, would send an HTTP POST against the
route. Where a command needs data, the command will query the route's schema
and ask the user to enter the data.
        '''
        try:
            global g_links
            g_links = get_routes(line, server)
            print()
            for link in g_links.links:
                Utilities().print_link(link)
        except Exception as e:
            error = Utilities().error_handler(
                        error_text='{0}'.format(str(e))
                    )
            pprint(error)


def do_command(method='GET', line=None):
    data, header = Utilities().do_method(
        method=method,
        command=line, 
        links=g_links
    )
    print()
    for t in sorted(header):
        print(t, header[t])
    print()
    pprint(data)


#
# Main module
#
if __name__ == '__main__':
    App.prompt = ' >> '
    App.intro = 'Command line microservice interpreter. Remember to '+\
                    'set the server using: server <servername>'

    App().cmdloop()
