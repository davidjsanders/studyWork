#from flask import Flask, Blueprint, abort
#from flask_restful import Api, Resource, url_for
#
from flask_restful import Resource

class HelloDavid(Resource):
    def get(self):
        return {'output':'Hello David!'}

