import json
from flask import Response
from Methods import Methods
from Links import Link

class Utilities(object):
    def error_handler(
         self,
         error_severity='error',
         error_text=None,
         error_data=None,
         error_status=400
        ):

        return {error_severity:
            {"message":error_text,
             "status":error_status,
             "data":error_data
            }}

    def print_link(self, link=None):
        if link == None or type(link) != Link:
            raise Exception('print_link: Link supplied is not a link!')

        print(link.identifier, link.description)
        print('{0}'.format('='*80))
        print('URL:       ', link.href)
        print('Methods:   ', str(link.methods))
        print('Schema:    ', str(link.schema))
        print('Parameters:',str(link.parameters))
        print()
        print()


    def do_method(self, method=None, command=None, links=None):
        if (not type(method) == str \
        and not type(command) == str) \
        or method == None \
        or command == None \
        or links == None:
            raise Exception('{0} {1} is invalid!'.format(method, command))

        if not method.upper() in ['GET','PUT','POST','DELETE','OPTIONS','HEAD']:
            raise Exception('{0} is an invalid method!'.format(method))

        args = command.split()
        if len(args) < 1:
            raise Exception('correct usage: get <route>, where <route> '+\
                            'is a number.')
        if links == []:
            raise Exception('The routes command must be executed before {0}'\
                            .format(method))
        command = int(command)

        try:
            route = int(command)

            if route < 0:
                raise ValueError("The route cannot be less than zero.")
            elif len(links.links) < 1:
                raise IndexError("There are no routes. The commands "+\
                                 "server <http://server> and routes "+\
                                 "must be executed before {0}"\
                                 .format(method))
            elif route >= len(links.links):
                error = "The route {0} doesn't exist. ".format(route)+\
                        "Run routes to view available routes."
                raise IndexError(error)
            if not method in links.links[route].methods:
                raise Exception('HTTP 405 - This route does not support {0}'\
                                .format(method))

            methods = Methods()
            if method.upper() == 'GET':
                data_set, headers = methods.get(links, command)
            elif method.upper() == 'PUT':
                data_set, headers = methods.put(links, command)
            elif method.upper() == 'POST':
                data_set, headers = methods.post(links, command)
            elif method.upper() == 'DELETE':
                data_set, headers = methods.delete(links, command)
            elif method.upper() == 'OPTIONS':
                data_set, headers = methods.options(links, command)
            elif method.upper() == 'HEAD':
                data_set, headers = methods.head(links, command)
            else:
                raise Exception('Sorry, {0} is not currently supported.'\
                                .format(method))

            return data_set, headers

        except Exception as e:
            error = Utilities().error_handler(
                        error_text='{0}'.format(str(e))
                    )
#            pprint(error)
            return error, []

