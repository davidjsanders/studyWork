import requests
import sys
from pprint import pprint

def routes_available(test_title, source_url):
    print('')
    print(test_title)
    print('')
    result = requests.get(source_url)
    data = result.json()
    print('{0:40s} {1:40s} {2:30s}'.format('Description','Route','Method(s)'))
    print('{0:40s} {1:40s} {2:30s}'.format('-' * 40, '-' * 40, '-' * 20))
    for data_line in data['_links']:
        print('{0:40s} {1:40s} {2:30s}'.format( \
            data_line['description']
            ,data_line['href']
            ,repr(data_line['method'])
            ))
    routes = data['_links']
    for route in routes:
        if route['method'] == 'GET' \
        or 'GET' in route['method']:
            result = requests.get(route['href'])
            print('')
            print('{0:40s} {1:40s}'.format('Description','Route'))
            print('{0:81s}'.format('-' * 80))
            print('{0:40s} {1:40s}'.format(route['description'], route['href']))
            print('')
            pprint(result.json())
            if 'notification' in result.json():
                print('')
                print('Notification Fields')
                print('--------------------------------------------------')
                for json_field in result.json()['notification']:
                    if not json_field[0] == '_':
                        print('{0:15s}: {1}'.format(json_field, result.json()['notification'][json_field]))
#                        print(json_field, ':', result.json()['notification'][json_field])
    return

#print('')
#print('Test Execution Script')
#print('')
try:
    server = sys.argv[1]
#    server = 'http://localhost:5200/'
    routes_available('Display Routes Available', server)
    print('')
    print('')
    print('Done.')
except Exception as e:
    print('')
    print('Exception.')
    print(repr(e))

