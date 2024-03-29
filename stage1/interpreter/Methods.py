from Parameters import Parameter_List, Parameter
import Utilities

from marshmallow import Schema, fields, post_load
from jsonschema import validate, exceptions
from pprint import pprint
import json
import requests
import warlock

class Methods(object):

    def __get_schema(self, schema_url=None):
        try:
            if schema_url == None:
                return
#                raise KeyError('Schema url cannot be blank. It must be a '+\
#                    'URL to the schema.'\
#                    )

            r = requests.get(schema_url)

            if not r.status_code == 200:
                raise Exception('Schema not found at {0}'.format(schema_url))

            if 'success' in r.json():
                if 'data' in r.json()['success']:
                    return r.json()['success']['data']
            else:
                raise Exception('Schema not found. Expected {"success":{'+
                                '"data":{...schema...}} but found {0}'\
                                .format(r.json()))
        except Exception:
            raise

    def __fetch_data(self, url_string=None):
        if url_string == None:
            raise KeyError('A URL must be provided for __fetch_data')
        try:
            result = requests.get(url_string)
            if not result.status_code == 200:
                if 'error' in result.json():
                    if 'message' in result.json()['error']:
                        error_message = result.json()['error']['message']
                else:
                    error_message = 'HTTP {0}'.format(result.status_code)
                raise Exception(error_message)
            elif not 'json' in result.headers['content-type']:
                raise Exception('Expected JSON data but did not receive it.')

            data = result.json()

#            if 'success' in data:
#                if 'data' in data['success']:
#                    data = data['success']['data']
#                    if type(data) == list \
#                    and len(data) == 1:
#                        data = data[0]

            return data, result.headers
        except Exception:
            raise

    def post(self, link_collection=None, route_identifier=-1):
        try:
            temp = None
            route = int(route_identifier)
            post_route = link_collection.links[route]

            url_string = post_route.input_parameters()

            if not url_string == post_route.href:
                schema = post_route.get_schema()
                schema_properties = schema['properties']
                schema_required = schema['required']
                object_factory = warlock.model_factory(schema)

                data_dict = {}
                for key in schema_properties.keys():
                    data_dict[str(key)] = schema_properties[key]['default']

                temp = object_factory(**data_dict)

                temp = post_route.input_dataitems(
                       schema_properties,
                       schema_required,
                       temp,
                       update_mode=False)

            insert = requests.post(url_string,
                                   data=json.dumps(temp),
                                   headers={'Content-Type':'application/json'}
                     )

            return insert.json(), insert.headers

        except Exception as e:
            raise


    def put(self, link_collection=None, route_identifier=-1):
        try:
            temp = None
            route = int(route_identifier)
            put_route = link_collection.links[route]

            url_string = put_route.input_parameters()

            if not put_route.schema == None:
                raw_data, headers = self.__fetch_data(url_string)
                original_data = raw_data['success']['data']

                schema = put_route.get_schema()
                schema_properties = schema['properties']
                schema_required = schema['required']
                object_factory = warlock.model_factory(schema)

                temp = object_factory(**original_data)

                temp = put_route.input_dataitems(
                       schema_properties,
                       schema_required,
                       temp,
                       update_mode=True)
                print('Made it through if')

            update = requests.put(url_string,
                                  data=json.dumps(temp),
                                  headers={'Content-Type':'application/json'}
                     )

            return update.json(), update.headers
        except Exception as e:
            raise

    def get(self,
            link_collection=None,
            route_identifier=-1,
            parameters_needed=True):
        try:
            route = int(route_identifier)
            get_route = link_collection.links[route]

            url_string = get_route.input_parameters()

            original_data, headers = self.__fetch_data(url_string)
            return original_data, headers
        except Exception as e:
            raise

    def delete(self,
               link_collection=None,
               route_identifier=-1):
        try:
            route = int(route_identifier)
            del_route = link_collection.links[route]
            url_string = del_route.input_parameters()
            delete = requests.delete(url_string)

            return delete.json(), delete.headers
        except Exception:
            raise

    def options(self,
                link_collection=None,
                route_identifier=-1):
        try:
            route = int(route_identifier)
            opt_route = link_collection.links[route]

            url_string = opt_route.input_parameters()

            options = requests.options(url_string,
                                      headers={'Content-Type':'application/json'}
                     )

            allowed = Utilities.Utilities().error_handler(
                error_severity='success',
                error_data = options.headers['allow'],
                error_status = 200,
                error_text = 'Options for route {0}'.format(route)
            )

            return allowed, options.headers
        except Exception:
            raise

    def head(self,
             link_collection=None,
             route_identifier=-1):
        try:
            route = int(route_identifier)
            opt_route = link_collection.links[route]

            url_string = opt_route.input_parameters()

            options = requests.head(url_string,
                                    headers={'Content-Type':'application/json'}
                     )

            headers = Utilities.Utilities().error_handler(
                error_severity='success',
                error_data = dict(options.headers),
                error_status = 200,
                error_text = 'Headers for route {0}'.format(route)
            )

            return headers, options.headers
        except Exception:
            raise

