from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "hello_carscan"
app.config['MONGO_URI'] = "mongodb://localhost:27017/user_profiles"

# instantiating Mongo DB Connection to our application
mongo = PyMongo(app)


@app.route('/add_profile', methods=['POST'])
def add_user_profile():
    received_json = request.getjson()
    fname = received_json['fname']
    lname = received_json['lname']
    dob = received_json['dob']
    city = received_json['city']
    mobile = received_json['mobile']

    if fname and lname and dob and city and mobile:
        record_id = mongo.db.profiles.insert({
            'First Name': fname,
            'Last Name': lname,
            'Date Of Birth': dob,
            'City': city,
            'Mobile Number': mobile
        })

        resp = jsonify(f"User Profile Added Successfully with id : {record_id}")
        resp.status_code = 200
        return resp
    else:
        return something_went_wrong()


@app.route('/view_profiles')
def view_profiles():
    profiles = mongo.db.profiles.find()
    resp = dumps (profiles)
    return resp


@app.errorhandler(404)
def something_went_wrong(error=None):
    message = {
        'status': 404,
        'message': 'Not Found @' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


# App start point when run
if __name__ == "__main__":
    print("Welcome to the User Profiles API")
    # debug = True helps restart the server whenever a code change is saved
    app.run(debug=True)
