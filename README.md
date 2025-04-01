# ALU Nest 
## Overview
The ALU Student Housing Platform is a web application designed to simplify the process of finding affordable off-campus housing and compatible roommates for African Leadership University (ALU) students in Kigali, Rwanda. The platform addresses key challenges such as rising rental prices, lack of centralized housing information, and the difficulty of finding suitable roommates.

## Features
- User Management: Secure login/signup system 

- Housing Listings:
Create, edit, archive, and delete property listings
Search and filter listings based on preferences
Direct contact with property lister via email

- Roommate Matching:
Create detailed roommate profiles
Search and filter potential roommates
Profile activation/archiving functionality

- Neighborhood Comparison:
Side-by-side comparison of different areas
General housing and neighborhood information

## Technology Stack
- Backend
Python/Flask
MongoDB (with PyMongo)
Passlib for password hashing
Local filesystem for images

- Frontend
HTML5, CSS3, JavaScript
Flask templating (Jinja2)

- Development Tools
VS Code
Python virtual environment
MongoDB Atlas or Local MongoDB

## Setup Instructions
### Prerequisites
* Python 3.x installed
* MongoDB (either Atlas cloud service or local installation)
* VS Code (recommended) or other code editor

### Installation 
1. Clone the repository/download the project zip file 

2. Set up your virtual environment

3. Install dependencies 

4. Set up your own database with mongoDb Atlas/Local MongoDB 

5. Create your .env file that will have your credentials such as Mongo connection url and your secret flask key

6. Make sure you have the correct folders for image uploads and add placement images like /static/uploads/

7. Run the app with Python app.py 

## Common errors you might encounter: 

- Module not found error: Verify all dependencies are installed (pip install -r requirements.txt)

- File upload/path errors: Ensure static/uploads folders exist, Include placeholder images for listings and profiles

- 400 errors: Typically API route issues,  check your backend routes

- UI not updating: Check JavaScript console for errors, Verify HTML templates are properly linked

- Database connection issues:Verify MongoDB is running, Check connection string in .env file

## User Guide 

1. Login/Signup
Use your email address to register 
Create secure password 

2. Dashboard 
Central hub after login
Access to all platform features
- Roommate Profile 
Create one profile per user
Include:Personal details, Roommate preferences, Budget range, Profile picture (optional)
Toggle profile visibility (archive/activate)

- House Listings 
Create multiple listings 
Include:Property details, Photos, Pricing, Availability
Options to: Archive (for temporary removal in the search bar for house listings), Edit, Delete (permanent removal)

3. Searching and Filtering 
- Housing Listings:Filter by preferences, View details, Contact lister via email prompt

- Roommate Profiles:Filter by compatibility, Contact via email prompt

4. Neigborhood Comparison 
Select two areas to compare
View side-by-side information
Access general housing resources

5. Navigation
Use header menu for all features
"About Us" section for guidance

6. Security 
Log out when done (header menu)
No dashboard access when logged out

## Future enhancements 
- Modularity: Implementing a modular design to accommodate future feature additions seamlessly.

- Authentication: Exploring alternative authentication methods, such as Google authentication, allowing users to log in or sign up using their assigned Google student emails for a smoother experience.

- House listings: Introducing a "share listing" option, enabling students to share listings they find with others who may be interested.

- Roommate profiles: Expanding preference options so students can better describe themselves and specify their ideal living conditions.

- Neighborhood estimates: Conducting real research to replace the current dummy data and including more neighborhoods in the comparison tool for a more comprehensive and accurate analysis.

## Contributors= Team 11
* Lilala Jemima Runiga
* Kolade Adepoju 
* Emmanuella Asoliya Briggs 
* Winston Nji 




