import os

class Environment(object):
    __env_obj = {
                  "server_name":None,
                  "port_number":None,
                  "ip_addr":None,
                  "version":"v1_00"
                }

    def __init__(self):
        self.server_name = self.__env_obj["server_name"] = self.__update_server_name()
        self.port_number = self.__env_obj["port_number"] = self.__update_port_number()
        self.ip_addr = self.__env_obj["ip_addr"] = self.__update_ip_addr()
        self.version = self.__env_obj["version"] = self.__update_version()

    def __str__(self):
        return str(self.__env_obj)


    def __repr__(self):
        return self.__str__()


    def __getitem__(self, key):
        return_value = None
        try:
            return_value = self.__env_obj[key]
        except KeyError as ke:
            raise KeyError('The environment variable {0} '.format(key)+\
                           'is not defined.')
        return return_value


    def __iter__(self):
        for key in self.__env_obj:
            yield {key:self.__env_obj[key]}


    def get_env(self):
        return self.__env_obj


    def update_env(self):
        self.__env_obj["server_name"] = self.__update_server_name()
        self.__env_obj["port_number"] = self.__update_port_number()
        self.__env_obj["ip_addr"] = self.__update_ip_addr()
        self.__env_obj["version"] = self.__update_version()


    def __update_server_name(self):
        server_name = None

        try:
            server_name = os.environ['serverName']
        except KeyError as ke:
            server_name = 'localhost'
        except Exception:
            pass

        return server_name

    def __update_port_number(self):
        port_number = None

        try:
            port_number = os.environ['portToUse']
        except KeyError as ke:
            port_number = '5000'
        except Exception:
            pass

        return port_number

    def __update_ip_addr(self):
        ip_addr = None

        try:
            ip_addr = os.environ['hostIP']
        except KeyError as ke:
            ip_addr = '127.0.0.1'
        except Exception:
            raise

        return ip_addr


    def __update_version(self):
        version = None

        try:
            version = os.environ['version']
        except KeyError as ke:
            version = 'v1_00'
        except Exception:
            raise

        return version
