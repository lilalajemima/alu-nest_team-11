from flask import Flask, request, jsonify
from pymongo import MongoClient
from bcrypt import hashpw, gensalt
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['off_campus_housing']
students_collection = db['students']

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    # Get JSON data from request
    data = request.json
    full_name = data.get('fullName')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    # Check if user already exists
    if students_collection.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 400

    # Hash password using bcrypt
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    # Create user document
    user = {
        'full_name': full_name,
        'email': email,
        'password_hash': hashed_password,
        'phone': phone,
        'created_at': datetime.utcnow()
    }

    # Insert the user data into database
    students_collection.insert_one(user)
    return jsonify({'message': 'Registration successful'}), 201

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)