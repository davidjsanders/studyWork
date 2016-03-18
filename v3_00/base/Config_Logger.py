import json

class Config_Logger(object):
    __controller = None

    def __init__(self, control=None):
        if control == None:
            raise Exception('Control was not passed. Config_Logger cannot '+\
                            'initiate!')
        self.__controller = control


    def get_logger(self):
        success = 'success'
        status = '200'
        message = 'Central logging status.'

        logger = self.__controller.get_value('logger')
        if logger in ([], '', None):
            logger = None

        data = {'logger':logger}
        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def remove_logger(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            self.__controller.log('Remove Log request received.')
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            self.__controller.log('Remove Log request - validating JSON')
            json_data = json.loads(json_string)
            key = json_data['key']
            logger = self.__controller.get_value('logger')

            self.__controller.log('Remove Log request - validating key')
            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging key incorrect.')

            self.__controller.log('Remove Log request - validating logger '+\
                                  'is currently running.')
            if logger in (None, '', []):
                raise ValueError('The service is not logging, '+\
                                 'so central logging cannot be switched off.')

            self.__controller.log('Remove Log request - clearing logger')
            self.__controller.clear_value('logger')
            self.__controller.logger.set_central_logger(None)
            data = {'logger':None}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except Exception as e:
            self.__controller.log('Exception: {0}'.format(repr(e)))

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)
        self.__controller.log("Set Log request - response: "+\
                              "{0} - {1}. Message = {2}".\
                              format(status, data, message))
        self.__controller.log('Remove Log request completed.')

        return return_value


    def set_logger(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            self.__controller.log('Set Log request received')
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            self.__controller.log('Set Log request - validating JSON')
            json_data = json.loads(json_string)
            key = json_data['key']
            logger = json_data['logger']

            self.__controller.log('Set Log request - validating key')
            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging key incorrect.')

            self.__controller.log('Set Log request - setting logger')
            self.__controller.set_value('logger', logger)
            self.__controller.logger.set_central_logger(logger)
            data = {'logger':logger}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(ke)
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.__controller.log('Exception: {0}'.format(message))
            #raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)
        self.__controller.log("Set Log request - response: "+\
                              "{0} - {1}. Message = {2}".\
                              format(status, data, message))
        self.__controller.log('Set Log request completed.')

        return return_value

