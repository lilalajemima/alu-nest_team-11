from datetime import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bcrypt import hashpw, gensalt

app = Flask(__name__)

#For user registration
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['off_campus_housing']
students_collection = db['students']

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    # Get data from the request
    data = request.json
    full_name = data.get('fullName')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    # Check if the user already exists
    if students_collection.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 400

    # Hash the password
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    # Create a new user
    user = {
        'full_name': full_name,
        'email': email,
        'password_hash': hashed_password,
        'phone': phone,
        'created_at': datetime.utcnow()
    }

    # Save the user to the database
    students_collection.insert_one(user)
    return jsonify({'message': 'Registration successful'}), 201

#For roommate profile creation

@app.route('/roommate-profiles', methods=['GET'])
def search_roommate_profiles():
    budget = request.args.get('budget', type=float)
    lifestyle_preferences = request.args.getlist('lifestyle_preferences')
    study_habits = request.args.get('study_habits')
    interests = request.args.getlist('interests')

    query = {}
    if budget:
        query['roommate_profile.budget'] = {'$lte': budget}
    if lifestyle_preferences:
        query['roommate_profile.lifestyle_preferences'] = {'$all': lifestyle_preferences}
    if study_habits:
        query['roommate_profile.study_habits'] = study_habits
    if interests:
        query['roommate_profile.interests'] = {'$all': interests}

    profiles = list(students_collection.find(query, {
        '_id': 0,
        'full_name': 1,
        'roommate_profile.budget': 1,
        'roommate_profile.lifestyle_preferences': 1,
        'roommate_profile.study_habits': 1,
        'roommate_profile.interests': 1,
        'roommate_profile.bio': 1
    }))
    
    return jsonify(profiles), 200

# Run the app
if __name__ == '__main__':
    app.run()