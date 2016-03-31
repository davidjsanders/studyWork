import json

class v1_00_Config_Logger(object):
    controller = None

    def __init__(self, control=None, module=None):
        if control == None:
            raise Exception('Control was not passed. Config_Logger cannot '+\
                            'initiate!')
        self.controller = control
        self.module_name = module or 'Module'
        self.method_name = 'unknown'


    def get_logger(self):
        try:
            self.method_name = 'get_logger'
            success = 'success'
            status = '200'
            message = 'Central logging status.'
            data = None

            self.controller.log('{0}-{1}: Get Logger request received.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )
            logger = self.controller.get_value('logger')
            if logger in ([], '', None):
                logger = None

            data = {'logger':logger}
        except Exception as e:
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message, log_to_central=False)
            print(error_text)

        self.controller.log('{0}-{1}: Logger data set: {2}'\
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

    # UPDATED - 30 March 2016
    #           Ignore json.
    #
    def remove_logger(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            self.method_name = 'remove_logger'
            self.controller.log('{0}-{1}: Remove Log request received.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )

            logger = self.controller.get_value('logger')
            if logger in (None, '', []):
                raise ValueError('The service is not logging, '+\
                                 'so central logging cannot be switched off.')

            self.controller.log('{0}-{1}: Clearing logger.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )

            self.controller.clear_value('logger')

            data = {'logger':None}
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
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message)
            print(error_text)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.controller.log('{0}-{1}: Logger data set: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data),
            log_to_central=False
        )

        return return_value


    # UPDATED - 30 March 2016
    #           Validate logger parameter begins http:// note- doesn't
    #           mean the url is valid ONLY that it begins with http...
    #
    def set_logger(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            self.method_name = 'set_logger'
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
            logger = json_data['logger']

            self.controller.log('{0}-{1}: Validating Logger starts http://.'\
                .format(self.module_name,
                        self.method_name),
                log_to_central=False
            )
            if not logger[0:7] == 'http://':
                raise KeyError('Logger must begin http:// and point to a '+\
                               'valid central logging URL')

            self.controller.log('{0}-{1}: Setting Logger to {2}'\
                .format(self.module_name,
                        self.method_name,
                        logger),
                log_to_central=False
            )

            self.controller.set_value('logger', logger)
            data = {'logger':logger}
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
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message)
            print(error_text)

        self.controller.log('{0}-{1}: Logger data set: {2}'\
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

