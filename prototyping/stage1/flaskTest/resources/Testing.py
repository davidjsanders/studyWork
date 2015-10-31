from flask import Flask, Blueprint, abort
from flask_restful import Resource
import resources.Config as Config

class Testing(Resource):
    def get(self):
        #global testing_enabled

        if Config.testing_enabled:
            return({'Success':'It Worked!'})
        else:
            abort(404)


