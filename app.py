from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask (__name__)
app.secret_key = 'hello_carscan'
app.config['MONGO_URI'] = "mongodb://localhost:27017/user_profiles"

# instantiating Mongo DB Connection to our application
mongo = PyMongo (app)

# App start point when run
if __name__ == "__main__":
    print ("Welcome to the User Profiles API")
    # debug = True helps restart the server whenever a code change is saved
    app.run (debug=True)
