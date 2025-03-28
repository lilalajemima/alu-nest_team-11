from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  

# MongoDB credentials
connection_string = "mongodb+srv://emmanuellabriggs123:tvtopwGX7qC7a0GL@emma.ndgm6.mongodb.net/housingDB?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['housingDB']
collection = db['profiles']

# Getting all the profiles from the database collection?
@app.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = list(collection.find({}))
    for profile in profiles:
        profile['_id'] = str(profile['_id']) 
    return jsonify(profiles)

# Filtering the profiles for the search bar in the front end
@app.route('/profiles/filter', methods=['GET'])
def filter_profiles():
    filters = {}
    
    
    gender = request.args.get('gender')
    min_budget = request.args.get('minBudget')
    max_budget = request.args.get('maxBudget')
    personality = request.args.get('personality')
    
    
    if gender:
        filters['lookingFor'] = gender
    if min_budget:
        filters['budgetRange.min'] = {'$gte': int(min_budget)}
    if max_budget:
        filters['budgetRange.max'] = {'$lte': int(max_budget)}
    if personality:
        filters['personalityTrait'] = personality
    
    
    filtered_profiles = list(collection.find(filters))
    for profile in filtered_profiles:
        profile['_id'] = str(profile['_id']) 
    return jsonify(filtered_profiles)

if __name__ == '__main__':
    app.run(debug=True)