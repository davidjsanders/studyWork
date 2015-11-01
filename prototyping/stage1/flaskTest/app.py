#!/flask/bin/python3
from flask import Flask, Blueprint, abort
from flask_restful import Api
import resources.Config as Config
from resources.HelloWorld import HelloWorld
from resources.Testing import Testing
from resources.HelloDavid import HelloDavid
from resources.Message import Message, Messages, MessageSpecific

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/<string:message>', '/')
api.add_resource(Testing, '/testing')
api.add_resource(HelloDavid, '/David')
api.add_resource(Message, '/message/<string:key>')
api.add_resource(Messages, '/messages')
api.add_resource(MessageSpecific, '/id-<string:identifier>/message/<string:key>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
