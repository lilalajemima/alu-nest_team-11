from pymongo import MongoClient

# MongoDB connection string
connection_string = "mongodb+srv://emmanuellabriggs123:tvtopwGX7qC7a0GL@emma.ndgm6.mongodb.net/housingDB?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(connection_string)

# Use the database named 'housingDB'
db = client['housingDB']

# Define the collection name
collection_name = "collection_house-listings"
collection = db[collection_name]

# Dummy data to be inserted
dummy_data = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "rent_per_room_rwf": 120000,
        "num_bedrooms": 2,
        "num_bathrooms": 1,
        "furnished": True,
        "electricity_included": True,
        "security_guard": False,
        "water_included": True,
        "wifi_included": False,
        "washing_machine": False,
        "location": "Kwa Nayinzira",
        "description": "A cozy 2-bedroom house in Kwa Nayinzira, perfect for students. Close to public transport and local markets.",
        "images": [
            "house2-image1.jpg",
            "house2-image2.jpg",
            "house2-image3.jpg"
        ]
    },
]

# Insert the dummy data into the collection
try:
    result = collection.insert_many(dummy_data)
    print(f"Inserted {len(result.inserted_ids)} documents into the '{collection_name}' collection.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()