from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests
from pprint import pformat

class Config_Help_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def help(self):
        success = 'success'
        status = '200'
        message = 'Phone configuration commands.'
        data = None

        try:
            data = {"configuration":[
                       {"launch":
                           {"url":"config/launch/<string:app>",
                            "rel":"launch",
                            "methods":["post"],
                            "data":{"key":"string"}
                           }
                       },
                       {"location":
                           {"url":"config/location",
                            "rel":"location",
                            "methods":["get", "post"],
                            "data":{"key":"string", "x":"float", "y":"float"}
                           }
                       },
                       {"lock":
                           {"url":"config/lock",
                            "rel":"lock",
                            "methods":["get", "post"],
                            "data":{}
                           }
                       },
                       {"monitor":
                           {"url":"config/monitor",
                            "rel":"monitor",
                            "methods":["get", "post", "delete"],
                            "data":{"key":"string",
                                    "service":"string",
                                    "recipient":"string"}
                           }
                       },
                       {"pair":
                           {"url":"config/pair",
                            "rel":"pair",
                            "methods":["get", "post", "delete"],
                            "data":{"key":"string",
                                    "bluetooth":"string"}
                           }
                       },
                       {"push_notifications":
                           {"url":"config/push",
                            "rel":"push",
                            "methods":["post"],
                            "data":{"key":"string",
                                    "service":"string",
                                    "recipient":"string"}
                           }
                       }
                    ],
                   "operation":[
                       {"location":
                           {"url":"location",
                            "rel":"location",
                            "methods":["get"],
                            "data":{"key":"string"}
                           }
                       },
                       {"notification":
                           {"url":"notification",
                            "rel":"notification",
                            "methods":["post"],
                            "data":{"key":"string",
                                    "message":"string",
                                    "sender":"string",
                                    "action":"string"}
                           }
                       },
                    ]
                   }
            self.__controller.log('Command executed')
            self.__controller.log('-'*79)
            self.__controller.log('Command executed: Help')
            self.__controller.log('')
        except requests.exceptions.ConnectionError as rce:
            return {'success':'error',
                    'status':500,
                    'message':'Phone cannot communicate with the monitor '+\
                      'app running at {0}'.format(monitor_app)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'
                   }
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
        except Exception as e:
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


help_control_object = Config_Help_Control()


