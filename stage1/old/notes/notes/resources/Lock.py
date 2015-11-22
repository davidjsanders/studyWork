from notes import app,api

from flask_restful import Resource, reqparse
from flask import Flask, abort
import notes.resources.Config as Config
import sys

class Lock(Resource):
    def get(self):
        return {'locked':Config.locked}

    def put(self):
        Config.locked = True
        return {'locked':Config.locked}

class Unlock(Resource):
    def put(self, unlock_code):
        if unlock_code == Config.unlock_code:
            Config.locked = False
        return {'locked':Config.locked}

