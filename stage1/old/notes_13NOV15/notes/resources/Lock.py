from notes import app,api

from flask_restful import Resource, reqparse
from flask import Flask, abort
import notes.resources.Config as Config
import sys

class Lock(Resource):
    def get(self):
        return {'locked':Config.get_lock()}

    def put(self):
        return {'locked':Config.set_lock(True)}

class Unlock(Resource):
    def put(self, unlock_code):
        if unlock_code == Config.unlock_code:
            Config.set_lock(False)
            return {'locked':Config.get_lock()}
        else:
            return {'error':'bad unlock code.'}

