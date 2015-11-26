from marshmallow import Schema, fields, post_load
from jsonschema import validate
import json

# Load links schema
f = open('schemas/links.json','r')
__schema__ = json.load(f)
f.close()

class Link_Schema(Schema):
    description = fields.Str(required=True)
    identifier = fields.Int(required=True)
    href = fields.Str(required=False)
    rel = fields.Str(required=True)
    methods = fields.List(fields.Str())

    @post_load
    def make_link(self, data):
        return Link(**data)

class Link_Collection(object):
    def __init__(
        self
    ):
        self.links = []

    def parse_links(self, links=None):
        try:
            if links == None:
                raise Exception('The link list was empty.')

            # Define a sort function for the links list of objects
            # Reference -
            # http://pythoncentral.io/
            #   how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
            def getKey(item):
                return links[item]['identifier']

            for link in sorted(links, key=getKey):
                print('Validating...')
                validate(links[link], __schema__)
                new_link = Link_Schema(strict=True).load(links[link]).data
                self.links.append(new_link)
        except Exception as e:
            raise

class Link(object):
    def __init__(
        self,
        name=None,
        identifier=-1,
        description=None,
        href=None,
        rel=None,
        methods=[]
    ):
        self.name = name
        self.identifier = identifier
        self.description = description
        self.href = href
        self.rel = rel
        self.methods = methods

    def __repr__(self):
        return str(Link_Schema().dump(self).data).replace("'",'"')

