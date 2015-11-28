from flask_restful import Resource, Api
from notifications import app, api

from jsonschema import validate, exceptions
import notifications.resources.Notifications as Notifications
import json
from pprint import pprint

print('Step 1. Create the notifications')
print('{0}'.format('-'*132))
notes = []
note = Notifications.Notification(note='Test notification', action='do something', sensitivity='low')
note.id = 1
notes.append(note)
note2 = Notifications.Notification()
note2.id = 2
note2.note = 'David J. Sanders'
note2.action = 'Doing something else :)'
note2.sensitivity = None
notes.append(note2)
note2 = Notifications.Notification()
note2.id = 3
note2.load(note.dump())
note2.action = 'Still doing something else :)'
notes.append(note2)
print()

print('Step 2. Write to the file_handler')
print('{0}'.format('-'*132))
file_handler = open('output.json','w')
file_handler.write('[')
last_row = len(notes) - 1
for idx, n in enumerate(notes):
    output_string = n.dump()
    if not idx == last_row:
        output_string += ','
    print(output_string)
    file_handler.write(output_string)
print()

print('Step 3. Add bad data to the file')
print('{0}'.format('-'*132))
temp_string = ', {"notification":{"notes":"test", "actions":"test"}}'
print(temp_string)
file_handler.write(temp_string)
file_handler.write(']')
file_handler.close()
print()
 
print('Step 4. Read the file_handler and add it to the notes. Should give deep copies, i.e. new notifications')
print('{0}'.format('-'*132))
file_handler = open('output.json', 'r')
temp_data = json.load(file_handler)
file_handler.close()

file_handler = open('notifications/resources/Notification_Schema.json','r')
schema = json.load(file_handler)
file_handler.close()

for idx, row in enumerate(temp_data):
    try:
        temp = Notifications.Notification()
        temp.id = len(notes)+1
        temp.load(json.dumps(row))
        notes.append(temp)
        print('Added row. ID {0} with Notification "{1}"'.format(temp.id, temp.note))
    except exceptions.ValidationError as v:
        print('Unable to add a row with the ID '+str(temp.id)+'. ', v.message, ':')
        pprint(row)
        error_string = 'Schema requires: '
        for idx2, key in enumerate(temp.__schema__['required']):
            error_string += '\033[4m' + temp.__schema__['required'][idx2] + '\033[0m, '
            #print('Key: {0}. Description: {1}'.format(key, temp.__schema__['required'][idx2]))
            #print('Key: {0}. Description: {1}'.format(key, temp.__schema__['properties'][key]))
#        pprint(temp.__schema__['properties'])
        print(error_string)
        continue
    except Exception as e:
        print(str(e))
print()

print('Step 5. Iterate through all the notifications')
print('{0}'.format('-'*132))
for idx, n in enumerate(notes):
    print('Row {0}: id: {4}, note: "{1}", action: "{2}", sensitivity: "{3}"'.format(idx, n.note, n.action, n.sensitivity, n.id))

print()
print('Done.')
print()
