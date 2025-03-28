from pymongo import MongoClient

connection_string = "mongodb+srv://emmanuellabriggs123:tvtopwGX7qC7a0GL@emma.ndgm6.mongodb.net/housingDB?retryWrites=true&w=majority"

client = MongoClient(connection_string)

db = client['housingDB']  

collection = db['profiles']  

sample_data = [
    {
        "name": "Jane Doe",
        "gender": "Female",
        "nationality": "Rwandan",
        "degreeProgram": "BSE",
        "intake": "Sept 2023",
        "personalityTrait": "Ambivert",
        "lookingFor": "Female",
        "budgetRange": { "min": 250000, "max": 350000 },
        "description": "I’m a second-year BSE student who loves reading, cooking, and occasional movie nights. I prefer a quiet environment but enjoy socializing occasionally. Looking for a roommate who is clean and respectful.",
        "email": "janedoe@example.com",
        "profileImage": "https://via.placeholder.com/150"
    },
    {
        "name": "John Smith",
        "gender": "Male",
        "nationality": "Kenyan",
        "degreeProgram": "BEL",
        "intake": "Jan 2024",
        "personalityTrait": "Extrovert",
        "lookingFor": "Male",
        "budgetRange": { "min": 300000, "max": 400000 },
        "description": "I’m an outgoing BEL student who enjoys sports, music, and exploring new places. I’m looking for a roommate who is easygoing and shares similar interests.",
        "email": "johnsmith@example.com",
        "profileImage": "https://via.placeholder.com/150"
    },
    {
        "name": "Alice Johnson",
        "gender": "Female",
        "nationality": "Nigerian",
        "degreeProgram": "IBT",
        "intake": "March 2023",
        "personalityTrait": "Introvert",
        "lookingFor": "Female",
        "budgetRange": { "min": 200000, "max": 300000 },
        "description": "I’m a quiet and focused IBT student who enjoys reading, coding, and spending time indoors. I’m looking for a roommate who respects personal space and is tidy.",
        "email": "alicejohnson@example.com",
        "profileImage": "https://via.placeholder.com/150"
    },
    {
        "name": "Michael Brown",
        "gender": "Male",
        "nationality": "South African",
        "degreeProgram": "BSE",
        "intake": "Sept 2022",
        "personalityTrait": "Ambivert",
        "lookingFor": "No preference",
        "budgetRange": { "min": 280000, "max": 380000 },
        "description": "I’m a final-year BSE student who enjoys both quiet nights in and social outings. I’m looking for a roommate who is easy to live with and shares similar values.",
        "email": "michaelbrown@example.com",
        "profileImage": "https://via.placeholder.com/150"
    },
    {
        "name": "Sarah Lee",
        "gender": "Female",
        "nationality": "Ghanaian",
        "degreeProgram": "BEL",
        "intake": "Jan 2023",
        "personalityTrait": "Extrovert",
        "lookingFor": "Female",
        "budgetRange": { "min": 220000, "max": 320000 },
        "description": "I’m a lively BEL student who loves meeting new people, traveling, and trying new foods. I’m looking for a roommate who is fun and adventurous.",
        "email": "sarahlee@example.com",
        "profileImage": "https://via.placeholder.com/150"
    }
]

collection.insert_many(sample_data)

print("Data is inserted")