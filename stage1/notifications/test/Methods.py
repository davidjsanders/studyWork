from marshmallow import Schema, fields, post_load
from jsonschema import validate
from pprint import pprint
import json
import requests

class Methods(object):

    def __parameters(self, url, parameter_collection = []):
        __url_string = url

        if parameter_collection == []:
            return url

        for p in parameter_collection:
            print('Please enter the following parameters:')
            while True:
                try:
                    input_value = input('  '+p['name']+' : ')
                    if p['type'] == int:
                        input_value = int(input_value)

                    if not input_value == None\
                    or not p['required']:
                        __parameter = __url_string[\
                            __url_string.index('<'):__url_string.index('>')+1]
                        __url_string = __url_string.replace\
                            (__parameter, str(input_value))
                        break
                except ValueError as ve:
                    print('  Invalid value provided. {0} needs to be a {1}'\
                        .format(p['name'], repr(p['type'])))
                    pass
                except Exception:
                    raise

        return __url_string

    def get(self, link_collection=None, route_identifier=-1):
        try:
            route = int(route_identifier)

            if route < 0:
                raise ValueError("The route cannot be less than zero.")
            elif route > len(link_collection.links):
                raise IndexError("The route doesn't exist. Have you run routes?")
            if not 'GET' in link_collection.links[route].methods:
                raise Exception('HTTP 405 - This route does not support GET')

            if not link_collection.links[route].parameters == []:
                result = requests.get(self.__parameters(
                         link_collection.links[route].href,
                         link_collection.links[route].parameters))
            else:
                result = requests.get(link_collection.links[route].href)

            print()
            headers = result.headers

            if not result.status_code == 200:
                if 'error' in result.json():
                    if 'message' in result.json()['error']:
                        error_message = result.json()['error']['message']
                else:
                    error_message = 'HTTP {0}'.format(result.status_code)
                raise Exception(error_message)
            elif not 'json' in result.headers['content-type']:
                raise Exception('Expected JSON data but did not receive it.')

            data_set = result.json()

            if 'success' in data_set:
                if 'data' in data_set['success']:
                    data_set = data_set['success']['data']
                    if type(data_set) == list \
                    and len(data_set) == 1:
                        data_set = data_set[0]

            return data_set, headers
        except Exception as e:
            raise
