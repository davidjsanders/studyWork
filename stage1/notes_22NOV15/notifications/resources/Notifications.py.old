import marshmallow

class Notification_List(object):

    def __init__(self):
        self.notification_list = []

    def __repr__(self):
        return 'There are {0} notifications'.format(
                   str(len(self.notification_list)))

    def append(self, notification):
        if type(notification) != Notification:
            raise ValueError
        self.notification_list.append(notification)

    def iter_items(self):
        for note in self.notification_list:
            yield note.id, note

    def clear_items(self):
        self.notification_list = []

class Notification(object):

    def __init__(self
                ,note=None
                ,action=None
                ,sensitivity=None
                ,marshalled_data=None):
        self.id = -1
        self.related = [{'id':123, 'url':'http://www.msn.ca'},{'id':234}]
        if marshalled_data == None:
            self.note = note
            self.action = action
            self.sensitivity = sensitivity
        else:
            if type(marshalled_data) != marshmallow.schema.UnmarshalResult:
                print('Bad data type -> '+repr(type(marshalled_data)))
                return None
            self.note = marshalled_data.data['note']
            self.action = marshalled_data.data['action']
            self.sensitivity = marshalled_data.data['sensitivity']

    def __repr__(self):
        return 'Notification(<id={self.id!r})>'.format(self=self)

    def iter_fields(self):
        yield "ID", self.id
        yield "note", self.note
        yield "action", self.action
        yield "sensitivity", self.sensitivity

#    def to_json(self):
#        return_value = {'data':}
#        return_attributes = {
#            'note':note,
#            'action':action,
#            'sensitivity':sensitivity
#        }
#        return_related = {
#            'related':{
#            }
#        }
#        return_links = {
#            'links':{
#                'self':'https://localhost:5000/notifications/'+self.id,
#                'collection':'https://localhost:5000/notifications/'
#            }
#        }

