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

    def __input_dataitems(self, 
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
                            if update_mode:
                                break
                            if type(data_item[k]) == int:
                                break
                            temp = None

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
                    except warlock.InvalidOperation as io:
                        print(io)
                    except Exception as e:
                        print(repr(e))
            print()
            return data_item
        except Exception:
            raise

    def __parameters(self, url, parameter_collection = []):
        __url_string = url

        if parameter_collection == []:
            return url

        print('Please enter the following parameters:')
        for p in parameter_collection:
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
                    pass
                except Exception:
                    raise

        print()
        return __url_string

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

            if 'success' in data:
                if 'data' in data['success']:
                    data = data['success']['data']
                    if type(data) == list \
                    and len(data) == 1:
                        data = data[0]

            return data, result.headers
        except Exception:
            raise

    def post(self, link_collection=None, route_identifier=-1):
        try:
            route = int(route_identifier)
            put_route = link_collection.links[route]

            url_string = self.__parameters(put_route.href,put_route.parameters)

            schema = self.__get_schema(put_route.schema)
            schema_properties = schema['properties']
            schema_required = schema['required']
            object_factory = warlock.model_factory(schema)

            data_dict = {}
            for key in schema_properties.keys():
                data_dict[str(key)] = schema_properties[key]['default']

            temp = object_factory(**data_dict)

            temp = self.__input_dataitems(
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
            route = int(route_identifier)
            put_route = link_collection.links[route]

            url_string = self.__parameters(put_route.href,put_route.parameters)

            original_data, headers = self.__fetch_data(url_string)

            schema = self.__get_schema(put_route.schema)
            schema_properties = schema['properties']
            schema_required = schema['required']
            object_factory = warlock.model_factory(schema)

            temp = object_factory(**original_data)

            temp = self.__input_dataitems(
                       schema_properties,
                       schema_required,
                       temp,
                       update_mode=True)

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
            put_route = link_collection.links[route]

            url_string = self.__parameters(put_route.href,put_route.parameters)

            original_data, headers = self.__fetch_data(url_string)
            get_data = requests.get(url_string,
                                  headers={'Content-Type':'application/json'}
                     )


            return get_data.json(), headers
        except Exception as e:
            raise

    def delete(self,
               link_collection=None,
               route_identifier=-1):
        try:
            route = int(route_identifier)
            del_route = link_collection.links[route]

            url_string = self.__parameters(del_route.href, del_route.parameters)

            original_data, headers = self.__fetch_data(url_string)

            delete = requests.delete(url_string,
                                     headers={'Content-Type':'application/json'}
                     )

            return delete.json(), delete.headers
        except Exception:
            raise

    def options(self,
                link_collection=None,
                route_identifier=-1):
        try:
            route = int(route_identifier)
            opt_route = link_collection.links[route]

            url_string = self.__parameters(opt_route.href, opt_route.parameters)

            original_data, headers = self.__fetch_data(url_string)

            options = requests.options(url_string,
                                      headers={'Content-Type':'application/json'}
                     )

            return {'allowed':options.headers['allow']}, options.headers
        except Exception:
            raise

    def head(self,
             link_collection=None,
             route_identifier=-1):
        try:
            route = int(route_identifier)
            opt_route = link_collection.links[route]

            url_string = self.__parameters(opt_route.href, opt_route.parameters)

            original_data, headers = self.__fetch_data(url_string)

            options = requests.head(url_string,
                                    headers={'Content-Type':'application/json'}
                     )

            return {}, options.headers
        except Exception:
            raise

