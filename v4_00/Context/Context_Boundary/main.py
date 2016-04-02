from Context import app, api
from Context.Control import global_controller
from Context_Boundary.Sample_Boundary import Sample_Boundary
#
# Get the version of the API
#
version = global_controller.get_value('version')

api.add_resource(Sample_Boundary, '/{0}/sample'.format(version))

# Reference: Adamo, D. [2015], 'Handling CORS Requests in Flask(-RESTful) APIs'
# [ONLINE]. Available at: http://www.davidadamojr.com/handling-cors-requests-in-flask-restful-apis/
# (Accessed: 08 March 2016)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Authorization, Accept')
    response.headers.add('Access-Control-Allow-Methods',
        'GET,PUT,POST,OPTIONS,HEAD,DELETE')
    return response


### Generated path for service: State
from Context_Boundary.State_Boundary import State_Boundary
api.add_resource(State_Boundary, '/{0}/state'.format(version))

### Generated path for service: Query
from Context_Boundary.Query_Boundary import Query_Boundary
api.add_resource(Query_Boundary, '/{0}/query'.format(version))

### Generated path for service: Notify
from Context_Boundary.Notify_Boundary import Notify_Boundary
api.add_resource(Notify_Boundary, '/{0}/notify'.format(version))

### Generated path for service: Subscribe
from Context_Boundary.Subscribe_Boundary import Subscribe_Boundary
api.add_resource(Subscribe_Boundary, '/{0}/subscribe'.format(version))
