from Links import Link_Collection
from Utilities import Utilities
from pprint import pprint

def get_routes(command, server=None):
    try:
        if server == None:
            raise Exception('Server must be set using: server <servername>')

        g_links = Link_Collection()

        args = command.split()
        verbose = False
        if len(args) > 0:
            if args[0] == '--verbose':
                verbose = True
            else:
                raise Exception('correct usage: routes <--verbose>, '+\
                                 'where <--verbose> displays full details.')

        g_links.get_links(server.server_name)
        return g_links

    except Exception as e:
#        error = Utilities().error_handler(
#                    error_text='{0}'.format(str(e))
#                )
        raise Exception(e)

