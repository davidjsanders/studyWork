from marshmallow import Schema, fields, post_load
from jsonschema import validate
import json
import requests

# Load links schema
f = open('schemas/links.json','r')
__schema__ = json.load(f)
f.close()

class Link_Schema(Schema):
    description = fields.Str(required=True)
    identifier = fields.Int(required=True)
    href = fields.Str(required=False)
    schema = fields.Str(required=False)
    rel = fields.Str(required=True)
    methods = fields.List(fields.Str())

    @post_load
    def make_link(self, data):
        return Link(**data)

class Link_Collection(object):
    def __init__(
        self
    ):
        self.links = []

    def get_links(self, server_name=None):
        try:
            if server_name == None:
                raise Exception('Server name is not set.')

            result = requests.get(server_name)
            json_data = result.json()

            if not result.status_code == 200\
            or not 'success' in json_data\
            or not 'data' in json_data['success']\
            or 'error' in result.json():
                raise Exception('The server issued a bad response.')

            links = json_data['success']['data']['_links']

            if links == None:
                raise Exception('The link list was empty.')

            # Define a sort function for the links list of objects
            # Reference -
            # http://pythoncentral.io/
            #   how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
            def getKey(item):
                return links[item]['identifier']

            self.links = []
            for link in sorted(links, key=getKey):
                validate(links[link], __schema__)
                new_link = Link_Schema(strict=True).load(links[link]).data
                self.links.append(new_link)
        except Exception as e:
            raise

class Link(object):
    def __init__(
        self,
        name=None,
        identifier=-1,
        description=None,
        href=None,
        schema=None,
        rel=None,
        methods=[]
    ):
        self.name = name
        self.identifier = identifier
        self.description = description
        self.href = href
        self.schema = schema
        self.rel = rel
        self.methods = methods
        self.parameters = []

        self.parameters = self.__parse_parameters(href)

    def __repr__(self):
        return str(Link_Schema().dump(self).data).replace("'",'"')

    def __parse_parameters(self, url=None):
        parameter_list =[]
        __url_string = url

        if url == None:
            return

        count = 0
        while True:
            try:
                if '<' in __url_string:
                    start_position = __url_string.index('<')
                    end_position = __url_string[start_position:].index('>')+1
                    parameter_string = __url_string[start_position:(start_position+end_position)]
                    name_start_position = parameter_string.index(':')+1
                    parameter_name = parameter_string[name_start_position:-1]
                    parameter_type = parameter_string[1:name_start_position-1]
                    parameter_type = str if parameter_type == 'string' else int
                    __url_string = __url_string.replace(parameter_string, '')
                    parameter_list.append({ \
                        'id':count,
                        'name':parameter_name,
                        'type':parameter_type,
                        'required':True
                    })
                    count += 1
                    print(parameter_string, parameter_name, __url_string)
                else:
                    break
            except ValueError as ve:
                break
        return parameter_list

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


