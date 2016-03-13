from Phone import app, api
from Phone_Boundary.Location_Boundary import Location_Boundary
from Phone_Boundary.Notification_Boundary import Notification_Boundary

api.add_resource(Location_Boundary, '/v1_00/location')
api.add_resource(Notification_Boundary, '/v1_00/notification')


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

