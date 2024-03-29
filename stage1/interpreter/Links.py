from Parameters import Parameter_List, Parameter

from marshmallow import Schema, fields, post_load
from jsonschema import validate, exceptions
import json
import requests
from warlock import InvalidOperation # For exception handling only

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
            if not result.status_code == 200: 
                raise Exception('The server issued a bad response: '+\
                          str(result.json()))

            json_data = result.json()

            if not result.status_code == 200\
            or not 'success' in json_data\
            or not 'data' in json_data['success']\
            or not '_links' in json_data['success']['data']\
            or 'error' in result.json():
                raise Exception('The server issued a bad response: '+\
                          str(result.json()))

            links = json_data['success']['data']['_links']

            if links == None:
                raise ValueError('The link list was empty.')

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
        except ValueError as ve:
            raise Exception(
                      'The server response was badly formed. Is this a '+\
                      'supported service? It must provide links based on the '+\
                      'links.json schema. Error reported was: '+str(ve)
                  )
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
        self.parameters = [] # Makes sure that parameters is always defined.

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
                    parameter_string = __url_string[start_position:\
                        (start_position+end_position)]
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
                else:
                    break
            except ValueError as ve:
                break
        return parameter_list

    def input_parameters(self):
        if self.parameters == []:
            return self.href
        if self.href == None:
            raise Exception('input_parameters: URL cannot be None')

        __url_string = self.href
        print('Please enter the following parameters:')
        for p in self.parameters:
            while True:
                try:
                    input_value = input('  '+p['name']+' : ')
                    if p['type'] == int:
                        input_value = int(input_value)

                    if not (input_value == None or input_value == '')\
                    or not p['required']:
                        __parameter = __url_string[\
                            __url_string.index('<'):__url_string.index('>')+1]
                        __url_string = __url_string.replace\
                            (__parameter, str(input_value))
                        break
                    else:
                        raise ValueError()
                except ValueError as ve:
                    print('  Invalid value provided. {0} needs to be a {1}'\
                          .format(p['name'], \
                          'string' if p['type'] == str else 'int'\
                         )
                    )
                except Exception:
                    raise
        return __url_string

    def input_dataitems(self, 
                        schema_properties=None, 
                        schema_required=None,
                        data_item=None,
                        update_mode=False
    ):
        if schema_properties == None:
            raise KeyError('A dict of schema properties must be provided.')
        if data_item == None:
            raise KeyError("For some reasons (this shouldn't happen), there "+\
                "is no data item.")

        print('This request requires data...')
        try:
            for k in schema_properties.keys():
                while True:
                    try:
                        if not k in data_item:
                            break
                        if type(data_item[k]) == None:
                            break

                        prompt_string = '  '+k+\
                            ' ('+schema_properties[k]['description']+')'
                        if update_mode:
                            prompt_string += ' [' + str(data_item[k]) + ']'
                        prompt_string += ': '

                        temp = input(prompt_string)

                        if k in schema_required \
                        and temp == ''\
                        and not update_mode:
                            raise ValueError('{0} is a required property.'\
                                .format(k))
                        elif temp == '':
                            break

                        if type(data_item[k]) == int:
                            data_item[k] = int(temp)
                        else:
                            data_item[k] = temp
                        break
                    except ValueError as ve:
                        if type(data_item[k]) == int:
                            print('{0} must be an integer number'\
                                .format(k))
                        else:
                            print(ve)
                    except TypeError as te:
                        print(te)
                    except KeyError:
                        raise
                    except InvalidOperation as io:
                        print(io)
                    except Exception as e:
                        print(repr(e))
            print()
            return data_item
        except Exception:
            raise

    def get_schema(self):
        try:
            if self.schema == None:
                return

            r = requests.get(self.schema)

            if not r.status_code == 200:
                raise Exception('Schema not found at {0}'.format(self.schema))

            if 'success' in r.json():
                if 'data' in r.json()['success']:
                    return r.json()['success']['data']
            else:
                raise Exception('Schema not found. Expected {"success":{'+
                                '"data":{...schema...}} but found {0}'\
                                .format(r.json()))
        except Exception:
            raise


