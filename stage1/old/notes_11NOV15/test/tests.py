#
# Reference: Argparse Tutorial - https://docs.python.org/2/howto/argparse.html#id1
#
import argparse
import requests
import sys
import json
from pprint import pprint

interactive = False
notification_url = ""
notifications_url = ""
lock_url = ""
unlock_url = ""
notification_last_insert = -1

def check_continue():
    if interactive:
        response = input('Press enter to continue, Q to quit...')
        if response.upper() == 'Q':
            print()
            print('Exiting...')
            print()
            sys.exit()

def print_header(text, decorator='-'):
    print('')
    print('')
    print('{0:79s}'.format(decorator*79))
    print('{0:1s} {1:76s}{0:1s}'.format(decorator, text))
    print('{0:79s}'.format(decorator*79))
    print('')


def routes_available(source_url, quiet_mode=False):
    result = requests.get(source_url)
    data = result.json()
    if not quiet_mode:
        print('{0:39s} {1:39s}'.format('Description','Route'))
        print('{0:39s} {1:39s}'.format('','Method(s)'))
        print('{0:39s} {1:39s}'.format('-' * 39, '-' * 39))
    for data_line in data['_links']:
        if data_line['href'][-12:] == 'notification':
            global notification_url
            notification_url = data_line['href']
        elif data_line['href'][-4:] == 'lock':
            global lock_url
            lock_url = data_line['href']
        elif data_line['href'][-11:] == 'unlock/9999':
            global unlock_url
            unlock_url = data_line['href']
        elif data_line['href'][-13:] == 'notifications':
            global notifications_url
            notifications_url = data_line['href']
        if not quiet_mode:
            print('{0:39s} {1:40s}'.format( \
                data_line['description']
               ,data_line['href']
                ))
            print('{0:40s}{1:40s}'.format( \
                ''
               ,repr(data_line['method'])
                ))
    routes = data['_links']
    if not quiet_mode:
        print()
        print('Notification URL : ', notification_url)
        print('Notifications URL: ', notifications_url)
        print('Lock URL         : ', lock_url)
        print('Unlock URL       : ', unlock_url)
        print()
        check_continue()
    return routes

def traverse(source_url):
    result = requests.get(source_url)
    routes = result.json()['_links']
    for route in routes:
        if 'GET' in route['method']:
            result = requests.get(route['href'])
            print_header('curl -X GET '+route['href'], '*')
            pprint(result.json())
            if 'notification' in result.json():
                print('')
                print('Notification Fields')
                print('--------------------------------------------------')
                for json_field in result.json()['notification']:
                    if not json_field[0] == '_':
                        print('{0:15s}: {1}'.format(
                            json_field
                           ,result.json()['notification'][json_field]))
            print('')
    check_continue()

def create_notification(note, action, sensitivity='', quiet_mode=False):
    if notification_url == "":
        print()
        print('Error. There is no notification add url')
        print()
        return

    if not quiet_mode:
        print('Notification data is:')
        print('{')
        print('    "note":"'+note+'", ')
        print('    "action":"'+action+'",')
        print('    "sensitivity":"'+sensitivity+'"')
        print('}')
        print()
        print('Executing curl...')

    json_data = {'note':note, 'action':action, 'sensitivity':sensitivity}
    headers = {'Content-Type':'application/json'}
    result = requests.post(notification_url
                          ,data=json.dumps(json_data)
                          ,headers=headers)
    result_data = result.json()

    if not quiet_mode:
        print()
        print('Result:')
    if 'error' in result_data:
        print('')
        print('Error received: ', result_data['error'])
    else:
        if not quiet_mode:
            pprint(result_data)
        global notification_last_insert
        notification_last_insert = int(result_data['notification']['identifier'])
    if not quiet_mode:
        print()
        check_continue()
    return notification_last_insert

def update_notification(note, action, sensitivity=''):
    if notification_url == "" \
    or notification_last_insert == -1:
        print()
        print('Error. There is no notification add url or notification to '+\
              'update')
        print()
        return

    result = requests.get(notification_url+'/'+str(notification_last_insert))
    result_data = result.json()

    print('Existing notification data is:')
    print('{')
    print('    "note":"'+result_data['notification']['note']+'", ')
    print('    "action":"'+result_data['notification']['action']+'",')
    print('    "sensitivity":"'+result_data['notification']['sensitivity']+'"')
    print('}')
    print()
    print('New notification data is:')
    print('{')
    print('    "note":"'+note+'", ')
    print('    "action":"'+action+'",')
    print('    "sensitivity":"'+sensitivity+'"')
    print('}')
    print()
    print('Executing curl...')

    json_new_data = {'note':note, 'action':action, 'sensitivity':sensitivity}

    headers = {'Content-Type':'application/json'}
    result = requests.put(notification_url+'/'+str(notification_last_insert)
                          ,data=json.dumps(json_new_data)
                          ,headers=headers)
    result_data = result.json()

    print()
    print('Result:')
    if 'error' in result_data:
        print('')
        print('Error received: ', result_data['error'])
    else:
        pprint(result_data)
    print()
    check_continue()

def delete_last_notification():
    if notification_url == "" \
    or notification_last_insert == -1:
        print()
        print('Error. There is no notification url or notification to '+\
              'update')
        print('Notification URL is {0}'.format(notification_url))
        print('Notification Number is {0}'.format(notification_last_insert))
        print()
        return

    result = requests.delete(notification_url+'/'+str(notification_last_insert))
    result_data = result.json()

    print()
    print('Result:')
    if 'error' in result_data:
        print('')
        print('Error received: ', result_data['error'])
    else:
        print('Deleted notification {0}'.format(notification_last_insert))
        pprint(result_data)
    print()
    check_continue()

def lock_device():
    if lock_url == "":
        print()
        print('Error. There is no lock url')
        print()
        return

    result = requests.put(lock_url)
    result_data = result.json()
    pprint(result_data)
    check_continue()

def unlock_device():
    if unlock_url == "":
        print()
        print('Error. There is no unlock url')
        print()
        return

    result = requests.put(unlock_url.replace('9999','1234'))
    result_data = result.json()
    pprint(result_data)
    check_continue()

def get_notifications():
    if notifications_url == "":
        print()
        print('Error. There is no unlock url')
        print()
        return

    result = requests.get(notifications_url)
    result_data = result.json()
    pprint(result_data)
    check_continue()

def set_mode(mode):
    if notifications_url == "":
        print()
        print('Error. There is no unlock url')
        print()
        return

    result = requests.put(notifications_url.replace('notifications','mode')+'/'+str(mode))
    result_data = result.json()
    pprint(result_data)
    check_continue()


try:
    parser = argparse.ArgumentParser()
    parser.add_argument("server"
                       ,type=str
                       ,help="Fully qualified url for the device"+\
                             ", e.g. http://localhost:82/ **NOTE** "+\
                             "the port and closing / should be provided")
    parser.add_argument("-i", "--interactive"
                       ,help="run in interactive mode, prompting between "+\
                             "tests"
                       ,action="store_true")
#    group = parser.add_mutually_exclusive_group()
#    group.add_argument("-v", "--verbose"
#                       ,help="run in full mode with prompts "
#                       , action="store_true")
#    group.add_argument("-m", "--minimal"
#                       ,help="run in minimal mode with no prompts)"
#                       ,action="store_true")
    args = parser.parse_args()
    if args.server:
        server = args.server
    if args.interactive:
        interactive = True

    print_header('Welcome to the ubicomp simulation tests', '=')

    old_interactive = interactive
    interactive = False

    print_header('Initialize. Call the device and find the routes available', '=')
    routes = routes_available(server, quiet_mode=True)

    print_header('Pre-tests. Create sample notifications', '#')
    inserted_list = []
    inserted_list.append(create_notification(
        note='Sample one'
       ,action='Do something'
       ,sensitivity='normal'
       ,quiet_mode=True))
    inserted_list.append(create_notification(
        note='Sample two'
       ,action='Something else'
       ,sensitivity='low'
       ,quiet_mode=True))
    inserted_list.append(create_notification(
        note='Note #3'
       ,action='Third activity'
       ,sensitivity='normal'
       ,quiet_mode=True))
    inserted_list.append(create_notification(
        note='Highly sensitive'
       ,action='4th Test'
       ,sensitivity='high'
       ,quiet_mode=True))
    inserted_list.append(create_notification(
        note='Another high sensitivity'
       ,action='nothing'
       ,sensitivity='high'
       ,quiet_mode=True))

    interactive = old_interactive
    check_continue()

    print_header('Test 1. Call the device and find the routes available', '=')
    routes = routes_available(server)

    print_header('Test 2. Iterate through the routes available', '=')
    traverse(server)

    print_header('Test 3. Create a new notification', '=')
    create_notification(note='Test Notification', action='Do something')

    print_header('Test 4. Update the new notification ('+\
                 str(notification_last_insert)+')', '=')
    update_notification(note='Updated notification'
                       ,action='Updated action'
                       ,sensitivity='high')

    print_header('Test 5. Delete the notification ('+\
                 str(notification_last_insert)+')', '=')
    delete_last_notification()

    print_header('Test 6. Lock the device', '=')
    lock_device()

    print_header('Test 7. Get notifications when locked [Default Mode]', '=')
    get_notifications()

    print_header('Test 8. Set Mode to 1', '=')
    set_mode(1)

    print_header('Test 9. Get notifications when locked [Mode 1]', '=')
    get_notifications()

    print_header('Test 10. Set Mode to 3', '=')
    set_mode(3)

    print_header('Test 11. Get notifications when locked [Mode 3]', '=')
    get_notifications()

    print_header('Test 12. Set Mode to 2', '=')
    set_mode(2)

    print_header('Test 13. Get notifications when locked [Default Mode]', '=')
    get_notifications()

    print_header('Test 14. Unlock the device', '=')
    unlock_device()

    print_header('Post-test tidy up', '#')
    old_interactive = interactive
    interactive = False
    for note in inserted_list:
        global notification_last_insert
        notification_last_insert = note
        delete_last_notification()
    interactive = old_interactive
    check_continue()

    print('Done.')
except Exception as e:
    print('')
    print('Exception.')
    print(repr(e))

