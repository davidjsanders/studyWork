from flask_restful import Resource
import notes.resources.Config as Config

class Modes(Resource):
    def put(self, mode):
        try:
            if mode < 1 or mode > 3:
                raise ValueError(
                    'Invalid mode ('+str(mode)+') requested. '+\
                    'Should be 1, 2, or 3.')
            Config.set_app_mode(mode)
        except Exception as e:
            return {'error':repr(e)}
        
        return {'mode':mode}

class ModesGet(Resource):
    def get(self):
        try:
            return {'mode':Config.get_app_mode()}
        except Exception as e:
            return {'error':repr(e)}
