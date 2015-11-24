# Import marshmallow for light weight serialization & de-serialization
from marshmallow import Schema, fields, post_load, post_dump

# Import jsonschema for Schema validation
from jsonschema import validate, exceptions, Draft3Validator

# Import Notification module
from notifications.resources.Notifications import Notification

# Import JSON for JavaScript Object Notation serialization
import json

class Notifications(object):
    __nl_schema_file__ = 'schemas/Notification_List_Schema.json'

    def __init__(self):
        self.__iter_index = 0
        self.__notification_list = []

    def push(self
            ,note=None
            ,action=None
            ,sensitivity=None
            ,identifier=-1):
        self.__notification_list.append(Notification(note,action,sensitivity))
        if identifier == -1:
            note_list = len(self.__notification_list)
            if note_list > 1:
                self.__notification_list[-1].identifier = \
                    self.__notification_list[-2].identifier + 1
            elif note_list == 1:
                self.__notification_list[-1].identifier = 1
        else:
            self.__notification_list[-1].identifier = identifier

        return self.__notification_list[-1].identifier

    def pop(self):
        if len(self.__notification_list) < 1:
            raise IndexError('pop from empty list')
        del(self.__notification_list[:1])

    def dump(self):
        __nl_schema__ = Notification.Notification_Schema(many=True)
        return str(__nl_schema__.dump(self.__notification_list).data)\
            .replace("'",'"').replace('None','null')

    def load(self, json_data=None, validate_schema=False, strict=False):
        self.__notification_list = []
        error_count = 0
        error_text = ''

        if json_data == None or not type(json_data) == list:
            raise SyntaxError('JSON data must be passed to load as a list')

        if validate_schema:
            try:
                f = open(self.__nl_schema_file__,'r')
                list_schema = json.load(f)
                f.close()
                validate(json_data, list_schema)
            except exceptions.ValidationError as ve:
                error_count = 1
                error_text = \
                    'The json data failed to validate against the schema. '+\
                    ve.message + '\n'
            except Exception as e:
                raise
            finally:
                f.close()

            if strict:
                raise TypeError(error_text)

        for note in json_data:
            try:
                new_id = self.push()
                note_to_load = str(note)\
                    .replace("'",'"')\
                    .replace('None','null')
                self.__notification_list[self.index(new_id)]\
                    .load(note_to_load)
            except exceptions.ValidationError as ve:
                error_count += 1
                error_text += 'Error ' + str(error_count - 1) + ': ' + \
                    ve.message + '\n'
                del(self.__notification_list[self.index(new_id)])
        if error_count > 0:
            error_text = '\n\n\033[1m\033[4m' + \
                'Warnings occurred during data loading.\033[0m\n\n' +\
                error_text
            raise exceptions.ValidationError(error_text)

    def __len__(self):
        return len(self.__notification_list)

    def __iter__(self):
        for note in self.__notification_list:
            yield note

    def index(self, index):
        if not type(index) == int:
            raise TypeError('{0} is not a number. Index must be a number'\
                .format(index))
        for idx, note in enumerate(self.__notification_list):
            if note.identifier == index:
                return idx
        raise ValueError('{0} is not in list.'.format(index))

    def __getitem__(self, index):
        if not type(index) == int:
            raise TypeError('{0} is not a number. Index must be a number'\
                .format(index))
        if index > self.__notification_list[-1].identifier \
        or index < self.__notification_list[0].identifier:
            raise IndexError('Notification {0} does not exist.'\
                .format(index))
        try:
            index_position = self.index(index)
        except ValueError as v:
            raise IndexError('Notification {0} does not exist.'\
                .format(index))
        return self.__notification_list[index_position]


