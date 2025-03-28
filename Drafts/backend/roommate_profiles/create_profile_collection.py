from pymongo import MongoClient

connection_string = "mongodb+srv://emmanuellabriggs123:tvtopwGX7qC7a0GL@emma.ndgm6.mongodb.net/housingDB?retryWrites=true&w=majority"


client = MongoClient(connection_string)

db = client['housingDB']  # Use the database named 'housingDB'


collection_name = 'collections_profiles'


if collection_name in db.list_collection_names():
    print(f"Collection '{collection_name}' already exists.")
else:
    
    db[collection_name].insert_one({
        "name": "John Doe",
        "profileImage": "https://example.com/image.jpg",
        "degreeProgram": "Computer Science",
        "intake": "Fall 2023",
        "personalityTrait": "Introvert",
        "budgetRange": {
            "min": 50000,
            "max": 100000
        },
        "lookingFor": "Male",
        "description": "I am a quiet and organized person.",
        "email": "john.doe@example.com"
    })
    print(f"Collection '{collection_name}' created and document inserted!")


print("Collections in the database:")
print(db.list_collection_names())