from flask import flask
from flask_restful import Api, Resource


app = Flask(__name__)
# Api instance
api = Api(app)

# create subclass of Resource
class Newsletter(Resource):
    def get(self):
        return {"Newsletter": "It's a beautiful 108 out in Austin today."}

# can pass multiple URLs to the add_resource() method on the Api object
api.add_resource(Newsletter, '/newsletters')


if __name__ = '__main__':
    app.run(port=5555)


# can access the data from command line with curl
# $ curl http://127.0.0.1:5555
