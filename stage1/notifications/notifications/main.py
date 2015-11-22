from flask_restful import Resource, Api
from notifications import app, api

import notifications.resources.Notifications as Notifications
from jsonschema import exceptions
import json
from pprint import pprint

print('Step 1. Create the notifications')
print('{0}'.format('-'*132))
notes = []
note = Notifications.Notification(
    note='This is a notification', action='With an action which does something', sensitivity='low')
note.identifier = 1
notes.append(note)
note2 = Notifications.Notification()
note2.identifier = 2
note2.note = 'A second notification'
note2.action = 'Which does something else'
note2.sensitivity = None
notes.append(note2)
note3 = Notifications.Notification()
note3.identifier = 3
note3.note= 'A third notification'
note3.action = 'A third action'
note3.action = 'high'
notes.append(note3)
print()

print('Step 2. Write to the file')
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
 
print('Step 4. Read the file and add it to the notes. Should give deep copies, i.e. new notifications')
print('{0}'.format('-'*132))
file_handler = open('output.json', 'r')
temp_data = json.load(file_handler)
file_handler.close()

for idx, row in enumerate(temp_data):
    try:
        temp = Notifications.Notification()
        temp.identifier = len(notes)+1
        temp.load(json.dumps(row))
        notes.append(temp)
        print('Added row. ID {0} with Notification "{1}"'.format(temp.identifier, temp.note))
    except exceptions.ValidationError as v:
        print()
        print('\033[1m\033[4mValidation error\033[0m.')
        print('{0}'.format(v.message))
        continue
    except Exception as e:
        print()
        print('General exception {0}'.format(str(e)))
print()

print('Step 5. Iterate through all the notifications')
print('{0}'.format('-'*132))
for idx, n in enumerate(notes):
    print('Row {0}: id: {4}, note: "{1}", action: "{2}", sensitivity: "{3}"'\
        .format(idx, n.note, n.action, n.sensitivity, n.identifier))

print()
print('Done.')
print()
