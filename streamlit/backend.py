from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import datetime
import bcrypt
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Get secret key from .env

# MongoDB Atlas connection
client = MongoClient(os.getenv('MONGO_URI'))  # Get MongoDB URI from .env
db = client['your_database_name']  # Replace with your database name
users_collection = db['users']
obstacles_collection = db['obstacles']  # Collection for obstacles

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists!"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user
    new_user = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    users_collection.insert_one(new_user)
    return jsonify({"message": "User created successfully!"}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "User not found!"}), 404

    # Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"message": "Invalid password!"}), 401

    # Create JWT token
    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({"token": token}), 200

# Add Obstacle route
@app.route('/add_obstacle', methods=['POST'])
def add_obstacle():
    data = request.json

    # Prepare the document to insert
    obstacle_doc = {
        "email": data["email"],
        "description": data["description"],
        "status": data["status"],
        "location": data["location"],
        "timestamp": data["timestamp"]
    }

    # Handle photo upload
    if "photo" in data:
        # Decode the base64 photo
        photo_data = data["photo"]
        photo_bytes = base64.b64decode(photo_data)
        photo_filename = f"obstacle_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        
        # Save the photo to the filesystem (optional)
        with open(os.path.join("uploads", photo_filename), "wb") as f:
            f.write(photo_bytes)

        # Add the filename to the document
        obstacle_doc["photo"] = photo_filename

    # Insert the document into MongoDB
    obstacles_collection.insert_one(obstacle_doc)

    return jsonify({"message": "Obstacle added successfully!"}), 201

# Run the app
if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    app.run(debug=True)