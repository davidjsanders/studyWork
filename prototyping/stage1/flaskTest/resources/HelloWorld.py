from flask import Flask, Blueprint, abort
from flask_restful import Resource
import resources.Config as Config

class HelloWorld(Resource):
    def get(self, message=None):
        #global config.output_message
        if not message == None:
            abort(404)
        return {'output':Config.output_messages['message']}

    def put(self, message):
        Config.output_messages['message'] = message
        Config.testing_enabled = True
        return {'success':message}

