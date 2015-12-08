# Import Marshmallow for schema loading #
from marshmallow import Schema, fields, post_load

# Import jsonschema validator
from jsonschema import validate

def parse_links(links=None, schema=None):
    list_of_links = []
    try:
        if links == None \
            raise Exception('The link list was empty.')

        # Define a sort function for the links list of objects
        # Reference -
        # http://pythoncentral.io/
        #   how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
        def getKey(item):
            return links[item]['identifier']

        for link in sorted(_links, key=getKey):
            validate(links[link], schema)
            new_link = LinkSchema(strict=True).load(links[link]).data
            list_of_links.append(new_link)
    except Exception as e:
        raise
    return list_of_links

