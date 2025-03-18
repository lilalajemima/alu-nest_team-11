from pymongo import MongoClient

# MongoDB connection string
connection_string = "mongodb+srv://emmanuellabriggs123:tvtopwGX7qC7a0GL@emma.ndgm6.mongodb.net/housingDB?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(connection_string)

# Use the database named 'housingDB'
db = client['housingDB']

# Define the collection name
collection_name = "house_tips"
collection = db[collection_name]

# Sample data for house tips
sample_tips = [
    {
        "id": "tip-001",
        "user_id": "user-123",
        "label": "housing",
        "tip": "Always check the water pressure and plumbing before renting a house. It can save you a lot of hassle later."
    },
    {
        "id": "tip-002",
        "user_id": "user-456",
        "label": "neighborhood",
        "tip": "Visit the neighborhood at different times of the day to get a sense of noise levels and safety."
    },
    {
        "id": "tip-003",
        "user_id": "user-789",
        "label": "roommates",
        "tip": "Set clear boundaries and expectations with roommates early on to avoid conflicts."
    },
    {
        "id": "tip-004",
        "user_id": "user-123",
        "label": "other",
        "tip": "If you're moving to a new city, try to visit a few weeks before to explore the area and find the best housing options."
    }
]

# Insert the sample data into the collection
try:
    result = collection.insert_many(sample_tips)
    print(f"Inserted {len(result.inserted_ids)} documents into the '{collection_name}' collection.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()