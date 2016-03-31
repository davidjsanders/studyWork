from Test import app, api
from Test.Control import global_controller
from Test_Boundary.Sample_Boundary import Sample_Boundary
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

