import json, requests

class v1_00_Config_Context(object):
    controller = None

    def __init__(self, control=None, module=None):
        if control == None:
            raise Exception('Control was not passed. Config_Context cannot '+\
                            'initiate!')
        self.controller = control
        self.module_name = module or 'Module'
        print('Module name passed was {0}'.format(module))
        print('Module name set to {0}'.format(self.module_name))
        self.method_name = 'unknown'


    def get_context_engine(self):
        try:
            self.method_name = 'get_context'
            success = 'success'
            status = '200'
            message = 'Context Engine'
            data = None

            self.controller.log('{0}-{1}: Get Context request received.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )
            context = self.controller.get_value('context-engine')
            if context in ([], '', None):
                context = None

            data = {'context-engine':context}
        except Exception as e:
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message, log_to_central=False)
            print(message)

        self.controller.log('{0}-{1}: Context data set: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data),
            log_to_central=False
        )

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

    # UPDATED - 02 April 2016
    #           Remove context engine.
    #
    def clear_context_engine(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            self.method_name = 'remove_context'
            self.controller.log('{0}-{1}: Remove request received.'\
                .format(self.module_name,
                        self.method_name)
            )

            context = self.controller.get_value('context-engine')
            self.controller.log('{0}-{1}: Current context set to {2}'\
                .format(self.module_name,
                        self.method_name,
                        context)
            )
            if context in (None, '', []):
                raise ValueError('The service is not logging, '+\
                                 'so central logging cannot be switched off.')

            self.controller.log('{0}-{1}: Clearing context.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )

            self.controller.clear_value('context-engine')

            data = {'context-engine':None}
        except KeyError as ke:
            success = 'error'
            status = 400
            message = '{0}-{1}: Key Error >> {2}'\
                .format(self.module_name, self.method_name, str(ke))
            data = {'error-message':str(ke)}
            self.controller.log(message)
        except ValueError as ve:
            success = 'error'
            status = 400
            message = '{0}-{1}: {2}'\
                .format(self.module_name, self.method_name, str(ve))
            data = {'error-message':str(ve)}
            self.controller.log(message)
        except Exception as e:
            success = 'error'
            status = 500
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message)
            print(message)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.controller.log('{0}-{1}: Context data set: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data),
            log_to_central=False
        )

        return return_value


    # UPDATED - 30 March 2016
    #           Validate context parameter begins http:// note- doesn't
    #           mean the url is valid ONLY that it begins with http...
    # UPDATED - 02 April 2017
    #           Validate context engine can actually be reached.
    def set_context_engine(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            self.method_name = 'set_context'
            self.controller.log('{0}-{1}: Set Log request received.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )

            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            self.controller.log('{0}-{1}: Validating JSON.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )

            json_data = json.loads(json_string)
            context = json_data['context-engine']

            self.controller.log('{0}-{1}: Validating Context starts http://.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )
            if not context[0:7] == 'http://':
                raise KeyError('Context must begin http:// and point to a '+\
                               'valid central logging URL')

            response_returned = self.validate_context_engine(context)
            if not response_returned.status_code in (200,201):
                self.method_name = 'set_context'
                returned_data = \
                    json.loads(response_returned.data.decode('utf-8'))
                raise requests.exceptions.ConnectionError(
                    'Unable to contact context engine; therefore, '+\
                    'the context engine cannot be set to {0}.'.format(context)
                )

            self.controller.log('{0}-{1}: Setting Context to {2}'\
                .format(self.module_name,
                        self.method_name,
                        context),
                log_to_central=False
            )

            self.controller.set_value('context-engine', context)
            data = {'context-engine':context}
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        str(rce))
            self.controller.clear_value('context-engine')
            self.controller.log(message)
        except KeyError as ke:
            success = 'error'
            status = 400
            message = '{0}-{1}: Key Error >> {2}'\
                .format(self.module_name, self.method_name, str(ke))
            data = {'error-message':str(ke)}
            self.controller.log(message)
        except ValueError as ve:
            success = 'error'
            status = 403
            message = '{0}-{1}: {2}'\
                .format(self.module_name, self.method_name, str(ve))
            data = {'error-message':str(ve)}
            if loading_json:
                status = 400
                message = '{0}-{1}: {2}'\
                    .format(self.module_name,
                            self.method_name,
                            'The JSON data is badly formed. Please check')
                data = {'error-message':'Bad JSON data'}
            self.controller.log(message)
        except Exception as e:
            self.controller.clear_value('context-engine')
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message)
            print(message)

        self.controller.log('{0}-{1}: Context data set: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data),
            log_to_central=False
        )

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    # Added - 02 April 2016
    #         Validates context engine can actually be reached.
    #
    def validate_context_engine(self, context=None):
        validity='not set'
        try:
            self.method_name = 'validate_context_engine'
            success = 'success'
            status = '200'
            message = 'Context Engine'
            data = None

            self.controller.log('{0}-{1}: '\
                                   .format(self.module_name,
                                           self.method_name)+\
                                'Validate request received.'
            )

            if context in ([], '', None):
                raise ValueError('Context engine is not set.')

            self.controller.log('{0}-{1}: '\
                                   .format(self.module_name,
                                           self.method_name)+\
                                'Issuing get request to {0}.'.format(context)
            )
            request_response = requests.get(
                context,
                timeout=30
            )

            self.controller.log('{0}-{1}: '\
                                   .format(self.module_name,
                                           self.method_name)+\
                                'Request returned "{0}"'\
                                   .format(request_response)
            )

            if request_response.status_code not in (200,201):
                raise requests.exceptions.ConnectionError(
                    'Unable to communicate with context engine. Status '+\
                    'returned was {0}'.format(request_response.status_code)
                )

            validity='valid'
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = '{0}'\
                .format(str(ve))
            self.controller.log(message)
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = '{0}'\
                .format(str(rce))
            validity='invalid'
            self.controller.log(message)
        except Exception as e:
            success = 'error'
            status = '500'
            message = '{0}'\
                .format(repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message)
            print(message)

        data = {"context-engine":context,
                "validity":validity}

        self.controller.log('{0}-{1}: Context data set: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data),
            log_to_central=False
        )

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


