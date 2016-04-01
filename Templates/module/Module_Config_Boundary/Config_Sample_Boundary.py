from flask_restful import Resource, reqparse
from Module_Config_Control.Config_Sample_Control \
    import config_sample_control_object

class Config_Sample_Boundary(Resource):
    def get(self):
        return config_sample_control_object.sample_request()

    def post(self):
        #
        # Get the data with the request and decode it to UTF-8
        #
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        #
        # Don't return results immediately. There may be a need to update 
        # headers afterward SO, get the return result, do anything needed, and
        # then return.
        #
        return_state = config_sample_control_object.not_implemented('POST')

        # Return
        return return_state

    def put(self):
        #
        # Get the data with the request and decode it to UTF-8
        #
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        #
        # Don't return results immediately. There may be a need to update 
        # headers afterward SO, get the return result, do anything needed, and
        # then return.
        #
        return_state = config_sample_control_object.not_implemented('PUT')

        # Return
        return return_state

    def delete(self):
        #
        # Get the data with the request and decode it to UTF-8
        #
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        #
        # Don't return results immediately. There may be a need to update 
        # headers afterward SO, get the return result, do anything needed, and
        # then return.
        #
        return_state = config_sample_control_object.not_implemented('DELETE')

        # Return
        return return_state


