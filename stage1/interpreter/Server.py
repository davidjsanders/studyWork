# Class definitions
class Server(object):
    def __init__(
        self,
        server_name='http://localhost:5000/v1_00/'
    ):
        self.server_name = server_name

    def __repr__(self):
        return self.server_name


