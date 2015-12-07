from flask_restful import Resource, Api
from notifications import app, api

#import notifications.resources.Notifications as Notifications
from notifications.resources.Notifications import Notification
from jsonschema import exceptions
import json
from pprint import pprint

print('Step 1. Create the notifications')
print('{0}'.format('-'*132))
notes = []

note = Notification(
    note='This is a notification'
   ,action='With an action which does something'
   ,sensitivity='low')
note.identifier = 1
notes.append(note)
note = Notification(
    note='This is the second notification'
   ,action='Do this'
   ,sensitivity='high')
note.identifier = 2
notes.append(note)
note = Notification(
    note='This is third notification'
   ,action='Find something interesting'
   ,sensitivity='normal')
note.identifier = 3
notes.append(note)
note = Notification(
    note='This is a fourth notification'
   ,action='Watch television')
note.identifier = 4
notes.append(note)

for n in notes:
    print(n)
print()

print()
print('Step 2. Write to the file')
print('{0}'.format('-'*132))

temp = []
print('Writing...')
for n in notes:
    print(n.dump())
    temp.append(n.dump())

file_handler = open('output.json','w')
file_handler.write(json.dumps(temp))
file_handler.close()
print()

print()
print('Step 3. Load the original data back from the file and add three bad rows.')
print('{0}'.format('-'*132))
file_handler = open('output.json', 'r')
data_load = json.load(file_handler)
file_handler.close()
data_load.append(
    {'notification':{'note':'** BAD DATA ** this is a note'}}
)
data_load.append(
    {'notification':{'action':'** BAD DATA ** this is a note'}}
)
data_load.append(
    {'notification':{'note':'**BAD**', 'action':'**BAD**', 'sensitivity':'Nope'}}
)
file_handler.close()
print(data_load)
print()

print()
print('Step 4. Clear the notification list before loading.')
print('{0}'.format('-'*132))
notes = []
print('There are {0} notifications in the list'.format(len(notes)))
print()

print()
print('Step 5. Validate and load the data into the notification list.')
print('{0}'.format('-'*132))
for row in data_load:
    try:
        note = Notification()
        note.load(str(row))
        notes.append(note)
    except exceptions.ValidationError as ve:
        print(ve.message)
    except Exception as e:
        print(str(e))


print('Step 6. Iterate through all the notifications')
print('{0}'.format('-'*132))
for idx, n in enumerate(notes):
    print('Row {0}: id: {4}, note: "{1}", action: "{2}", sensitivity: "{3}"'\
        .format(idx, n.note, n.action, n.sensitivity, n.identifier))

print()
print('Done.')
print()
