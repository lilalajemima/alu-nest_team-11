from flask import Flask, render_template, session, redirect, request, jsonify, url_for, flash
from functools import wraps
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import uuid
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timezone 
from flask_wtf.csrf import CSRFProtect
from bson import ObjectId

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

###################################################################################################################################################################
# This the configuration for the file uploads 
#####################################################################################################################################################################

# For profile pictures
UPLOAD_FOLDER = 'static/uploads/profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#For house listings
HOUSE_IMAGES_FOLDER = 'static/uploads/house_images'
ALLOWED_HOUSE_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['HOUSE_IMAGES_FOLDER'] = HOUSE_IMAGES_FOLDER
os.makedirs(HOUSE_IMAGES_FOLDER, exist_ok=True)
PLACEHOLDER_IMAGE = 'house_placeholder.jpg'
app.config['PLACEHOLDER_IMAGE'] = PLACEHOLDER_IMAGE
PLACEHOLDER_IMAGE_PATH = os.path.join('static', 'images', 'house_placeholder.jpg')
app.config['PLACEHOLDER_IMAGE'] = PLACEHOLDER_IMAGE_PATH

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_house_image(filename):
    """Check if the house image has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_HOUSE_IMAGE_EXTENSIONS

def get_placeholder_image():
    """Ensure placeholder image exists or create a default one"""
    placeholder_path = os.path.join(app.root_path, app.config['PLACEHOLDER_IMAGE'])
    
    if not os.path.exists(placeholder_path):
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(placeholder_path), exist_ok=True)
            
            # Create a simple placeholder image if none exists
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (200, 200), color=(200, 200, 200))
            d = ImageDraw.Draw(img)
            d.text((10, 10), "House Image\nPlaceholder", fill=(0, 0, 0))
            img.save(placeholder_path)
        except ImportError:
            # If PIL isn't available, just ensure the directory exists
            os.makedirs(os.path.dirname(placeholder_path), exist_ok=True)
        except Exception as e:
            app.logger.error(f"Could not create placeholder image: {str(e)}")
    
    return placeholder_path

# Database setup
connection_string = "mongodb+srv://emmanuellabriggs123:tvtopwGX7qC7a0GL@emma.ndgm6.mongodb.net/housingDB?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client['housingDB']

# Static file cache busting
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# Login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        return redirect('/')
    return wrap

# User class
class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return redirect('/dashboard')

    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email already exists"}), 400
        if db.users.insert_one(user):
            return self.start_session(user)
        return jsonify({"error": "Signup failed"}), 400
    
    def login(self):
        user = db.users.find_one({"email": request.form.get('email')})
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid credentials"}), 401

    def signout(self):
        session.clear()
        return redirect('/')

# Initialize User
user = User()

class Profile:
    def get_profile(self, user_id):
        return db.profile.find_one({"user_id": user_id})
    
    def create_or_update_profile(self, user_id, data, picture_filename=None):
        profile_data = {
            "user_id": user_id,
            "name": data.get('name'),
            "gender": data.get('gender'),
            "nationality": data.get('nationality'),
            "intake": data.get('intake'),
            "degreeProgram": data.get('degreeProgram'),
            "budgetRange": {
                "min": int(data.get('budget_min', 0)),
                "max": int(data.get('budget_max', 0))
            },
            "lookingFor": data.get('lookingFor'),
            "personalityTrait": data.get('personalityTrait'),
            "description": data.get('description'),
            "updated_at": datetime.utcnow(),
            "archived": False
        }

        if picture_filename:
            profile_data['profilePicture'] = picture_filename
        
        existing_profile = self.get_profile(user_id)
        
        if existing_profile:
            # Update existing profile
            db.profile.update_one(
                {"user_id": user_id},
                {"$set": profile_data}
            )
        else:
            # Create new profile
            db.profile.insert_one(profile_data)
    
    def archive_profile(self, user_id, reason):
        db.profile.update_one(
            {"user_id": user_id},
            {"$set": {
                "archived": True,
                "archived_at": datetime.utcnow(),
                "archived_reason": reason
            }}
        )

# Initialize Profile
profile_manager = Profile()

#########################################################################################################################################################################
# Routes
#########################################################################################################################################################################
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/signup', methods=['POST'])
def signup():
    result = user.signup()
    if isinstance(result, tuple) and result[1] != 200:
        flash(result[0].json['error'])
        return redirect('/')
    return result

@app.route('/user/login', methods=['POST'])
def login():
    result = user.login()
    if isinstance(result, tuple) and result[1] != 401:
        flash(result[0].json['error'])
        return redirect('/')
    return result

@app.route('/user/signout')
def signout():
    return user.signout()

@app.route('/about')
def about():
    return render_template('about.html')

################################################################################################################################################################################################################################
# Dashboard Routes

################################################################################################################################################################################################################################

from bson import ObjectId
from flask import jsonify

@app.route('/dashboard/')
@login_required
def dashboard():
    user_id = session['user']['_id']
    profile = profile_manager.get_profile(user_id)
    
    # Convert house listings with proper ObjectId handling
    house_listings = []
    for listing in db.house_listing.find({"user_id": user_id}):
        listing['_id'] = str(listing['_id'])  # Convert ObjectId to string
        house_listings.append(listing)
    
    return render_template('dashboard.html', 
                         profile=profile, 
                         house_listings=house_listings)

@app.route('/dashboard/profile', methods=['POST'])
@login_required
def handle_profile():
    user_id = session['user']['_id']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'archive':
            reason = request.form.get('archived_reason', 'User initiated')
            profile_manager.archive_profile(user_id, reason)
            flash('Profile archived successfully', 'success')
            return redirect(url_for('dashboard'))
        
        # Handle file upload
        picture_filename = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '':  # User actually selected a file
                if file and allowed_file(file.filename):
                    try:
                        # Generate unique filename: userid_timestamp.ext
                        ext = file.filename.rsplit('.', 1)[1].lower()
                        filename = f"{user_id}_{int(datetime.now().timestamp())}.{ext}"
                        filename = secure_filename(filename)
                        
                        # Ensure upload directory exists
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        
                        # Save file
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        picture_filename = filename
                    except Exception as e:
                        flash('Error uploading profile picture', 'error')
                        app.logger.error(f"File upload error: {str(e)}")
                else:
                    flash('Invalid file type for profile picture', 'error')
                picture_filename = filename
        
        # Create/update profile
        try:
            profile_manager.create_or_update_profile(user_id, request.form, picture_filename)
            flash('Profile saved successfully', 'success')
        except Exception as e:
            flash('Error saving profile', 'error')
            app.logger.error(f"Profile save error: {str(e)}")
    
    return redirect(url_for('dashboard'))

@app.route('/uploads/profile_pictures/<filename>')
@login_required
def view_profile_picture(filename):
    """Serve uploaded profile pictures"""
    # Optional: Add security check to verify the user has access to this image
    return redirect(url_for('static', filename=f'uploads/profile_pictures/{filename}'))

@app.route('/remove-profile-picture', methods=['POST'])
@login_required
def remove_profile_picture():
    try:
        user_id = session['user']['_id']
        profile = db.profile.find_one({"user_id": user_id})
        
        if profile and 'profilePicture' in profile:
            # Delete the file
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile['profilePicture'])
            if os.path.exists(picture_path):
                os.remove(picture_path)
            
            # Update the profile
            db.profile.update_one(
                {"user_id": user_id},
                {"$unset": {"profilePicture": ""}}
            )
            
            return jsonify({"success": True})
        
        return jsonify({"success": False, "error": "No profile picture found"})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

####################################################################################################################################################################
#For dashboard house listings
#####################################################################################################################################################################

@app.route('/api/house_listings', methods=['GET', 'POST'])
def handle_house_listings():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    if request.method == 'GET':
        try:
            listings = list(db.house_listing.find({'user_id': session['user']['_id']}))
            for listing in listings:
                listing['_id'] = str(listing['_id'])
            return jsonify({'success': True, 'house_listings': listings})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
                files = []
            else:
                data = request.form.to_dict()
                files = request.files.getlist('house_images')

            # Validate required fields
            required_fields = ['rent_per_room_rwf', 'num_bedrooms', 'num_bathrooms', 'location']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

            # Process file uploads
            image_filenames = []
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['HOUSE_IMAGES_FOLDER'], filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    image_filenames.append(filename)

            # Use timezone-aware datetime
            current_time = datetime.now(timezone.utc)
            
            listing_data = {
                'user_id': session['user']['_id'],
                'rent_per_room_rwf': int(data['rent_per_room_rwf']),
                'num_bedrooms': int(data['num_bedrooms']),
                'num_bathrooms': int(data['num_bathrooms']),
                'location': data['location'],
                'description': data.get('description', ''),
                'furnished': data.get('furnished', 'false').lower() == 'true',
                'electricity_included': data.get('electricity_included', 'false').lower() == 'true',
                'security_guard': data.get('security_guard', 'false').lower() == 'true',
                'water_included': data.get('water_included', 'false').lower() == 'true',
                'wifi_included': data.get('wifi_included', 'false').lower() == 'true',
                'washing_machine': data.get('washing_machine', 'false').lower() == 'true',
                'status': data.get('status', 'available'),
                'images': image_filenames,
                'updated_at': current_time
            }

            # Handle update vs create
            if 'listing_id' in data and data['listing_id']:
                listing_id = ObjectId(data['listing_id'])
                db.house_listing.update_one(
                    {'_id': listing_id},
                    {'$set': listing_data}
                )
                message = 'Listing updated successfully'
            else:
                listing_data['created_at'] = current_time
                result = db.house_listing.insert_one(listing_data)
                listing_id = result.inserted_id
                message = 'Listing created successfully'

            listing_data['_id'] = str(listing_id)
            return jsonify({
                'success': True,
                'message': message,
                'listing': listing_data
            }), 201

        except ValueError as e:
            return jsonify({'success': False, 'error': f'Invalid number format: {str(e)}'}), 400
        except Exception as e:
            print("Error in /api/house_listings POST:", str(e))  # Debug logging
            return jsonify({'success': False, 'error': str(e)}), 500
        
@app.route('/api/house_listings/<listing_id>', methods=['GET'])
def get_house_listing(listing_id):
    try:
        listing = db.house_listing.find_one({
            '_id': ObjectId(listing_id),
            'user_id': session['user']['_id']
        })
        
        if not listing:
            return jsonify({'success': False, 'error': 'Listing not found'}), 404
        
        listing['_id'] = str(listing['_id'])
        return jsonify({'success': True, 'listing': listing})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/handle_house_listing', methods=['POST'])
def handle_house_listing():
    try:
        data = request.form.to_dict()
        
        listing_data = {
            'user_id': session['user']['_id'],
            'rent_per_room_rwf': int(data.get('rent_per_room_rwf', 0)),
            'num_bedrooms': int(data.get('num_bedrooms', 1)),
            'num_bathrooms': int(data.get('num_bathrooms', 1)),
            'location': data.get('location', ''),
            'description': data.get('description', ''),
            'furnished': 'furnished' in data,
            'electricity_included': 'electricity_included' in data,
            'security_guard': 'security_guard' in data,
            'water_included': 'water_included' in data,
            'wifi_included': 'wifi_included' in data,
            'washing_machine': 'washing_machine' in data,
            'status': data.get('status', 'available'),
            'updated_at': datetime.utcnow()
        }
        
        image_filenames = []
        for file in request.files.getlist('house_images'):
            if file and allowed_house_image(file.filename):
                filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                # Create full upload path - FIXED PATH CONSTRUCTION
                upload_path = os.path.join(app.root_path, 'static', 'uploads', 'house_images')
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                # Store just the filename, not the full path
                image_filenames.append(filename)
        
        if data.get('listing_id'):
            listing_id = ObjectId(data['listing_id'])
            
            if image_filenames:
                db.house_listing.update_one(
                    {'_id': listing_id},
                    {'$push': {'images': {'$each': image_filenames}}}
                )
            
            db.house_listing.update_one(
                {'_id': listing_id},
                {'$set': listing_data}
            )
        else:
            listing_data['images'] = image_filenames
            listing_data['created_at'] = datetime.utcnow()
            db.house_listing.insert_one(listing_data)
        
        flash('Listing saved successfully!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/api/house_listings/<listing_id>', methods=['DELETE'])
def delete_house_listing(listing_id):
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    try:
        # Verify listing exists and belongs to user
        listing = db.house_listing.find_one({
            '_id': ObjectId(listing_id),
            'user_id': session['user']['_id']
        })
        
        if not listing:
            return jsonify({'success': False, 'error': 'Listing not found'}), 404

        # Delete the listing
        result = db.house_listing.delete_one({'_id': ObjectId(listing_id)})
        
        # Delete associated images
        if 'images' in listing:
            for image in listing['images']:
                try:
                    os.remove(os.path.join(app.config['HOUSE_IMAGES_FOLDER'], image))
                except OSError:
                      continue
        
        return jsonify({'success': True, 'message': 'Listing deleted successfully'})

    except Exception as e:
        print(f"Error deleting listing: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/house_listings/<listing_id>/status', methods=['PUT'])
def update_listing_status(listing_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['available', 'rented', 'archived']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        result = db.house_listing.update_one(
            {'_id': ObjectId(listing_id), 'user_id': session['user']['_id']},
            {'$set': {'status': new_status, 'updated_at': datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            return jsonify({'success': False, 'error': 'Listing not found or status unchanged'}), 404
        
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/house_listings/<listing_id>/images', methods=['DELETE'])
def remove_listing_image(listing_id):
    try:
        data = request.get_json()
        image_name = data.get('image_name')
        
        if not image_name:
            return jsonify({'success': False, 'error': 'Image name required'}), 400
        
        result = db.house_listing.update_one(
            {'_id': ObjectId(listing_id), 'user_id': session['user']['_id']},
            {'$pull': {'images': image_name}}
        )
        
        if result.modified_count == 0:
            return jsonify({'success': False, 'error': 'Image not found or listing not found'}), 404
        
        try:
            os.remove(os.path.join(app.config['HOUSE_IMAGES_FOLDER'], image))
        except OSError as e:
            print(f"Error deleting image file: {e}")
        
        return jsonify({'success': True, 'message': 'Image removed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



#########################################################################################################################################################################
# This is for the roommate Search Routes
########################################################################################################################################################################

@app.route('/roommate-profiles')
@login_required
def roommate_profiles():
    # Base query for non-archived profiles
    query = {"archived": False}
    
    # Add filters from request args
    if request.args.get('gender'):
        query['gender'] = request.args.get('gender')
    if request.args.get('looking_for'):
        query['lookingFor'] = request.args.get('looking_for')
    if request.args.get('personality'):
        query['personalityTrait'] = request.args.get('personality')
    
    # Budget range filter
    min_budget = request.args.get('min_budget', type=int)
    max_budget = request.args.get('max_budget', type=int)
    
    if min_budget is not None or max_budget is not None:
        budget_query = {}
        if min_budget is not None:
            budget_query['$gte'] = min_budget
        if max_budget is not None:
            budget_query['$lte'] = max_budget
        query['budgetRange.min'] = budget_query
    
    # Get profiles + emails in one query
    profiles = list(db.profile.aggregate([
        {"$match": query},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$addFields": {
            "user_email": "$user.email"
        }}
    ]))
    
    return render_template('roommate_profiles.html', 
                         profiles=profiles,
                         current_user=session['user'])


########################################################################################################################################################################
# Neighborhood Information Routes
######################################################################################################################################################################

@app.route('/neighborhood')
@login_required
def neighborhood():  # Changed from neighborhood_info to neighborhood
    try:
        # Check if collection exists
        if 'neighborhood_info' not in db.list_collection_names():
            flash('Neighborhood data not available', 'error')
            return render_template('neighborhood.html', neighborhoods=[])
        
        # Get all unique neighborhood names
        neighborhoods = list(db.neighborhood_info.distinct("name"))
        
        if not neighborhoods:
            flash('No neighborhood data found', 'warning')
            
        return render_template('neighborhood.html', 
                            neighborhoods=neighborhoods,
                            error=None)
        
    except Exception as e:
        app.logger.error(f"Neighborhood error: {str(e)}")
        flash('Error loading neighborhood data', 'error')
        return render_template('neighborhood.html',
                            neighborhoods=[],
                            error=str(e))

@app.route('/api/neighborhood/<name>')
@login_required
def get_neighborhood_details(name):
    try:
        neighborhood = db.neighborhood_info.find_one({"name": name})
        if not neighborhood:
            return jsonify({"success": False, "error": "Neighborhood not found"}), 404
        
        # Convert ObjectId to string if it exists
        if '_id' in neighborhood:
            neighborhood['_id'] = str(neighborhood['_id'])
        
        return jsonify({
            "success": True,
            "neighborhood": neighborhood
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/compare-neighborhoods', methods=['POST'])
@login_required
def compare_neighborhoods():
    try:
        data = request.get_json()
        name1 = data.get('name1')
        name2 = data.get('name2')
        
        if not name1 or not name2:
            return jsonify({"success": False, "error": "Both neighborhood names are required"}), 400
        
        neighborhood1 = db.neighborhood_info.find_one({"name": name1})
        neighborhood2 = db.neighborhood_info.find_one({"name": name2})
        
        if not neighborhood1 or not neighborhood2:
            return jsonify({"success": False, "error": "One or both neighborhoods not found"}), 404
        
        # Convert ObjectIds to strings
        if '_id' in neighborhood1:
            neighborhood1['_id'] = str(neighborhood1['_id'])
        if '_id' in neighborhood2:
            neighborhood2['_id'] = str(neighborhood2['_id'])
        
        return jsonify({
            "success": True,
            "neighborhood1": neighborhood1,
            "neighborhood2": neighborhood2
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#########################################################################################################################################################################
# House Listings Public View Routes
#########################################################################################################################################################################

@app.route('/listings')
@login_required
def view_listings():
    # Base query for available listings
    query = {"status": "available"}
    
    # Add filters from request args
    location_filter = request.args.get('location')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    bedrooms = request.args.get('bedrooms', type=int)
    bathrooms = request.args.get('bathrooms', type=int)
    amenities = request.args.getlist('amenities')
    
    if location_filter:
        query['location'] = {"$regex": location_filter, "$options": "i"}
    
    if min_price is not None or max_price is not None:
        query['rent_per_room_rwf'] = {}
        if min_price is not None:
            query['rent_per_room_rwf']['$gte'] = min_price
        if max_price is not None:
            query['rent_per_room_rwf']['$lte'] = max_price
    
    if bedrooms:
        query['num_bedrooms'] = bedrooms
    
    if bathrooms:
        query['num_bathrooms'] = bathrooms
    
    # Handle amenities filters
    if amenities:
        for amenity in amenities:
            query[amenity] = True
    
    # Get listings with user emails
    listings = list(db.house_listing.aggregate([
        {"$match": query},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$addFields": {
            "user_email": "$user.email",
            "user_name": "$user.name"
        }},
        {"$sort": {"created_at": -1}}
    ]))
    
    # Convert ObjectId to string for each listing
    for listing in listings:
        listing['_id'] = str(listing['_id'])
    
    return render_template('listings.html', listings=listings)

@app.route('/listing/<listing_id>')
@login_required
def view_listing(listing_id):
    try:
        listing = db.house_listing.aggregate([
            {"$match": {"_id": ObjectId(listing_id)}},
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }},
            {"$unwind": "$user"},
            {"$addFields": {
                "user_email": "$user.email",
                "user_name": "$user.name"
            }}
        ]).next()
        
        if not listing:
            flash('Listing not found', 'error')
            return redirect(url_for('view_listings'))
        
        listing['_id'] = str(listing['_id'])
        return render_template('listing_detail.html', listing=listing)
    
    except StopIteration:
        flash('Listing not found', 'error')
        return redirect(url_for('view_listings'))
    except Exception as e:
        flash('An error occurred', 'error')
        return redirect(url_for('view_listings'))

if __name__ == '__main__':
    app.run(debug=True)