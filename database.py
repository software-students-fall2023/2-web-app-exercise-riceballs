from pymongo import MongoClient
from passlib.hash import sha256_crypt
import os
from dotenv import load_dotenv
load_dotenv()

mongodb_uri = os.getenv("MONGO_URI")
database_name = os.getenv("MONGO_DBNAME")

try:
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

client = MongoClient(mongodb_uri)
db = client[database_name]



def register_user(username, password):
    try:
        # check if user exist 
        ExistingUser = db.users.find_one({"username": username})
        if (ExistingUser):
            return False
        print(f"hi")
        # Insert user data into the 'users' collection
        hashed_password = sha256_crypt.encrypt(password)
        user_data = {"username": username, "password": hashed_password}
        db.users.insert_one(user_data)
        print(f"User registered: {user_data}")
        return True
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return False

def authenticate_user(username, password):
    user = db.users.find_one({"username": username})
    if user and sha256_crypt.verify(password, user['password']):
        return True
    return False