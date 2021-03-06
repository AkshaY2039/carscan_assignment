from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/user_profiles"

# instantiating Mongo DB Connection to our application
mongo = PyMongo(app)


# Method to Add New Profile Record
@app.route('/add_profile', methods=['POST'])
def add_user_profile():
    received_json = request.json
    fname = received_json['fname']
    lname = received_json['lname']
    dob = received_json['dob']
    city = received_json['city']
    mobile = received_json['mobile']

    if fname and lname and dob and city and mobile:
        record_id = mongo.db.profiles.insert_one({
            'fname': fname,
            'lname': lname,
            'dob': dob,
            'city': city,
            'mobile': mobile
        })

        resp = jsonify(f"User Profile Added Successfully")
        resp.status_code = 200
        return resp
    else:
        return something_went_wrong()


# Method to View All Profile Records Stored
@app.route('/view_profiles')
def view_profiles():
    profiles = mongo.db.profiles.find()
    resp = dumps(profiles)
    return resp


# Method to Update Single Profile Record
@app.route('/update_profile/<record_id>', methods=['PUT'])
def update_profile(record_id):
    received_json = request.json
    fname = received_json['fname']
    lname = received_json['lname']
    dob = received_json['dob']
    city = received_json['city']
    mobile = received_json['mobile']
    if fname and lname and dob and city and mobile:
        mongo.db.profiles.update_one(
            {'_id': ObjectId(record_id['$oid']) if '$oid' in record_id else ObjectId(record_id)},
            {'$set': {
                'fname': fname,
                'lname': lname,
                'dob': dob,
                'city': city,
                'mobile': mobile
        }})
        resp = jsonify("User Updated Successfully")
        resp.status = 200
        return resp
    else:
        return something_went_wrong()


# Method to Delete Single Profile Record
@app.route('/delete_profile/<record_id>', methods=['DELETE'])
def delete_profile(record_id):
    mongo.db.profiles.delete_one({'_id': ObjectId(record_id)})
    resp = jsonify("User Deleted Successfully")
    resp.status = 200
    return resp


# Method to View Single Profile Record
@app.route('/view_by_id/<record_id>')
def view_by_id(record_id):
    profile = mongo.db.profiles.find_one({'_id': ObjectId(record_id)})
    resp = dumps(profile)
    return resp

# Method to Search Records based on Given Criteria
@app.route('/search', methods=['GET'])
def search():
    received_json = request.json
    pairs = received_json.items()
    criteria = {}
    for key, value in pairs:
        criteria[key] = value
    profile = mongo.db.profiles.find(criteria)
    resp = dumps(profile)
    return resp


# Error Message Handling
@app.errorhandler(404)
def something_went_wrong(error=None):
    message = {
        'status': 404,
        'message': 'Not Found @ ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


# App start point when run
if __name__ == "__main__":
    print("Welcome to the User Profiles API")
    # debug = True helps restart the server whenever a code change is saved
    app.run()
