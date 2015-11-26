from marshmallow import Schema, fields, post_load
from jsonschema import validate
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

            result = requests.get(self.__parameters(
                         link_collection.links[route].href,
                         link_collection.links[route].parameters))

            print()
            headers = result.headers
            for header_item in headers:
                print('{0:20s} {1}'.format(header_item, headers[header_item]))
            print()

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
            data_keys = data_set.keys()
            print(data_set)
            print(data_keys)

        except Exception as e:
            print('error. '+str(e))

