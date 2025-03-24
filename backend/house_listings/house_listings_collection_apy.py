from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
connection_string = "mongodb+srv://emmanuellabriggs123:tvtopwGX7qC7a0GL@emma.ndgm6.mongodb.net/housingDB?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['housingDB']
collection = db['house_listings']

# Route to fetch all house listings
@app.route('/api/house-listings', methods=['GET'])
def get_house_listings():
    try:
        # Fetch all documents from the collection
        listings = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's default '_id' field
        return jsonify(listings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to filter house listings
@app.route('/api/house-listings/filter', methods=['GET'])
def filter_house_listings():
    try:
        # Get query parameters from the request
        min_rent = int(request.args.get('minRent', 0))
        max_rent = int(request.args.get('maxRent', float('inf')))
        bedrooms = request.args.get('bedrooms', 'any')
        location = request.args.get('location', 'any')
        amenities = request.args.getlist('amenities')  # List of amenities

        # Build the MongoDB query
        query = {
            "rent_per_room_rwf": {"$gte": min_rent, "$lte": max_rent},
        }
        if bedrooms != 'any':
            query["num_bedrooms"] = int(bedrooms)
        if location != 'any':
            query["location"] = location
        if amenities:
            for amenity in amenities:
                query[amenity] = True

        # Fetch filtered documents
        listings = list(collection.find(query, {'_id': 0}))
        return jsonify(listings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)