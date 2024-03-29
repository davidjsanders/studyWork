class Parameter_List(list):
    __parameters = []

    def __init__(self):
        pass

class Parameter(object):
    __parameter = {
        "id":"",
        "name":"",
        "type":"",
        "required":""
    }

    def __init__(
        self,
        parameter_id=None,
        parameter_name=None,
        parameter_type=None,
        parameter_required=False
    ):
        if parameter_id == None \
        or parameter_name == None \
        or parameter_type == None:
            raise Exception('Parameter<>.__init__: Parameter badly formed')

        self.__parameter['id'] = parameter_id
        self.__parameter['name'] = parameter_name
        self.__parameter['type'] = parameter_type
        self.__parameter['required'] = parameter_required

    def __str__(self):
        return str(self.__parameter)

    def get(self):
        return self.__parameter

    def put(self, parameter=None):
        if parameter == None or type(parameter) != dict:
            raise Exception('Parameter<>.put: Parameter is badly formed!')

