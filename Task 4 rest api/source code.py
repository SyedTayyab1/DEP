

from flask import Flask, request
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)

# Simulated in-memory database
users = {}

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username in users:
            return {"message": "User already exists"}, 400

        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        return {"message": "User created successfully"}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username not in users or not check_password_hash(users[username], password):
            return {"message": "Invalid credentials"}, 401
        
        # Normally, you'd return a token here. Simulated response for simplicity.
        return {"access_token": "fake-token-for-{}".format(username)}, 200

class ItemResource(Resource):
    def get(self, item_id):
        # Example logic to retrieve an item by ID
        item = {"item_id": item_id, "name": "Sample Item"}  # Replace with actual item retrieval logic
        return item, 200

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ItemResource, '/items/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret'  # Change this to a random secret key

  
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)

 

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Item

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400

        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401

class ItemResource(Resource):
    @jwt_required()
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return {'id': item.id, 'name': item.name, 'description': item.description}

    @jwt_required()
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, item_id):
        data = request.get_json()
        item = Item.query.get_or_404(item_id)
        item.name = data['name']
        item.description = data['description']
        db.session.commit()
        return {'id': item.id, 'name': item.name, 'description': item.description}

class ItemListResource(Resource):
    @jwt_required()
    def get(self):
        items = Item.query.all()
        return [{'id': item.id, 'name': item.name, 'description': item.description} for item in items]

    @jwt_required()
    def post(self):
        data = request.get_json()
        item = Item(name=data['name'], description=data['description'])
        db.session.add(item)
        db.session.commit()
        return {'id': item.id, 'name': item.name, 'description': item.description}, 201



