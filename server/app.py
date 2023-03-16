#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# 1. Create a homepage route
class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API", 
        }
        response = make_response(response_dict, 200)
        return response

api.add_resource(Home, '/')


# 2. return all records from newsletters table
class Newsletters(Resource):
    # instance method for each HTTP verb 

    # 3. get request
    def get(self):
        newsletters = Newsletter.query.all()

        response_dict = [newsletter.to_dict() for newsletter in newsletters]
        response = make_response(response_dict, 200)
        return response
    
    # 4. post request
    def post(self):
        # Postman > Body > raw > JSON
        new_n = Newsletter(
            title=request.get_json()["title"],
            body=request.get_json()["body"]
        )

        # Postman > Body > form-data
        # new_n = Newsletter(
        #     title=request.form['title'],
        #     body=request.form['body'],
        # )
        db.session.add(new_n)
        db.session.commit()
        
        response = make_response(new_n.to_dict(), 201)
        return response
api.add_resource(Newsletters, '/newsletters')



# 5. Retrieve a single record - by id
class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        response = make_response(newsletter.to_dict(), 200)
        return response
api.add_resource(NewsletterByID, '/newsletters/<int:id>')




if __name__ == '__main__':
    app.run(port=5555, debug=True)
