#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response, session
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pymongo
import datetime
from bson.objectid import ObjectId
import sys

from database import register_user, authenticate_user

# instantiate the app
app = Flask('FoodTruck')

app.secret_key = 'pass'

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
load_dotenv()  # take environment variables from .env.

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


# root page
@app.route('/FoodTruck')
def RootPage():
    User = session['username']
    return render_template('rootpage.html', User=User)

@app.route('/AddFoodTruck')
def AddFoodPage():
    User = session['username']
    return render_template('AddFoodTruck.html',  User=User, active_page='AddFoodTruck')

@app.route('/AddFoodTruck', methods=['POST'])
def addFoodTruck():
    
    if request.method == 'POST':
        FoodCartName = request.form['FoodCartName']
        Cuisine = request.form['Cuisine']
        Hours = request.form['Hours']
        Address = request.form['Address']
        Price = request.form['Price']
        Vegan = request.form['Vegan']
        User = session['username']

        FoodTruckData = {
            "User": User,
            "FoodCartName": FoodCartName,
            "Cuisine": Cuisine,
            "Hours": Hours,
            "Address": Address,
            "Price": Price,
            "vegan_options": Vegan
        }

        food_trucks_collection = db['food_trucks_information']
        food_trucks_collection.insert_one(FoodTruckData)
        return redirect(url_for('RootPage'))  
    


@app.route('/SearchCuisine')
def SearchCuisine():
    User = session['username']
    filteredFoodtruck = []
    food_trucks_collection = db['food_trucks_information']
    print(request.args.get("cuisine"))
    if request.args.get('cuisine') != None:
        cuisineQ = request.args['cuisine']
        print(cuisineQ)
        filteredFoodtruck = food_trucks_collection.find({
            "Cuisine":cuisineQ
        })
        return render_template('SearchCuisine.html', filteredFoodTruck = filteredFoodtruck,  User=User)
    else:
        filteredFoodtruck = food_trucks_collection.find()
        return render_template('SearchCuisine.html', filteredFoodTruck = [],  User=User, active_page='SearchCuisine')
            
    
@app.route('/ViewAllFood')
def ViewAllFood():
    User = session['username']
    food_trucks_collection = db['food_trucks_information']  # Assuming 'food_trucks' is your collection name
    all_food_trucks = food_trucks_collection.find()
    return render_template('ViewAllFood.html', all_food_trucks=all_food_trucks, User=User, active_page='ViewAllFood')

@app.route('/ViewMyFood')
def ViewMyFood():
    User = session['username']
    food_trucks_collection = db['food_trucks_information']
    AllMyFoodTrucks = food_trucks_collection.find({"User": session["username"]})
    return render_template('ViewMyFood.html', AllMyFoodTrucks=AllMyFoodTrucks, User=User, active_page='ViewMyFood')


@app.route('/DeleteTruck/<FoodTruckId>', methods=['POST'])
def DeleteTruck(FoodTruckId):
    food_trucks_collection = db['food_trucks_information']
    food_trucks_collection.delete_one({"_id": ObjectId(FoodTruckId)})
    return redirect(url_for('ViewMyFood'))


@app.route('/EditTruck/<FoodTruckId>', methods=['GET'])
def EditTruck(FoodTruckId):
    User = session['username']
    food_trucks_collection = db['food_trucks_information']
    TruckPage = food_trucks_collection.find({"_id": ObjectId(FoodTruckId)})
    return render_template('EditTruck.html', TruckPage=TruckPage, User=User)
    

# handle the edit page submissions 

@app.route('/EditTruck/<FoodTruckId>', methods=['POST'])
def EditTruckSubmission(FoodTruckId):
    if request.method == 'POST':
        FoodCartName = request.form['FoodCartName']
        Cuisine = request.form['Cuisine']
        Hours = request.form['Hours']
        Address = request.form['Address']
        Price = request.form['Price']
        Vegan = request.form['Vegan']
        User = session['username']

        FoodTruckData = {
            "User": User,
            "FoodCartName": FoodCartName,
            "Cuisine": Cuisine,
            "Hours": Hours,
            "Address": Address,
            "Price": Price,
            "vegan_options": Vegan
        }

        existingFoodTruck = db['food_trucks_information']
        existingFoodTruck.update_one({"_id": ObjectId(FoodTruckId) }, { "$set": FoodTruckData })
        return redirect(url_for('ViewMyFood'))
 
@app.route('/', methods=['GET', 'POST'])
def LoginPage():
    if (request.method == 'GET'):
        return render_template('Login.html', headerTitle = "Login", action = '/', register = True)
    else:
        username = request.form['fname']
        password = request.form['fpwd']

        if authenticate_user(username, password):
            # Authentication successful
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('RootPage'))
        else:
            error = "Login Falied: Invalid username or password."
            return render_template('Login.html', headerTitle="Login", action = '/',  register=True, error=error)
        

@app.route('/register', methods=['GET', 'POST'])
def RegisterPage():
    if request.method == 'GET':
        return render_template('Login.html', headerTitle="Register", action = '/register', register=False)
    else:
        name = request.form['fname']
        pwd = request.form['fpwd']
        
        if register_user(name, pwd):
            # Registration successful, print a message and redirect
            print(f"User '{name}' registered successfully.")
            return redirect(url_for('RootPage'))
        else:
            # Registration failed, print an error message
            print(f"Failed to register user '{name}'.")
            error =  'Username already exist please create a new one'
            return render_template('Login.html', headerTitle="Register", action = '/register', register=False, error=error)




app.run(host = '0.0.0.0', port = 8080)