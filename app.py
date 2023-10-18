#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response, session
from dotenv import load_dotenv
import os

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

# make a connection to db
# connection = pymongo.MongoClient("class-mongodb.cims.nyu.edu", 8080, )

# root page
@app.route('/FoodTruck')
def RootPage():
    return render_template('rootpage.html')

@app.route('/AddFoodTruck')
def AddFoodPage():
    return render_template('AddFoodTruck.html')

@app.route('/EditTruck')
def EditPage():
    return render_template('EditTruck.html')

@app.route('/individualFood')
def individualFood():
    return render_template('individualFood.html')

@app.route('/SearchCuisine')
def SearchCuisine():
    return render_template('SearchCuisine.html')

@app.route('/ViewAll')
def ViewAll():
    return render_template('ViewAll.html')


@app.route('/ViewMyFood')
def ViewMyFood():
    return render_template('ViewMyFood.html')

# # Login
# @app.route('/', methods = ['GET', 'POST'])
# def LoginPage():
#     if (request.method == 'GET'):
#         return render_template('Login.html', headerTitle = "Login", register = True)
#     else: 
#         name = request.form['fname']
#         pwd = request.form['fpwd']
#         if (name == pwd):  # perform validate login info via db !! PLACEHOLDER
#             return redirect(url_for('RootPage'))
#         else:
#             return render_template('Login.html', headerTitle = "Login", register = True)
    



@app.route('/', methods=['GET', 'POST'])
def LoginPage():
    error = None

    if request.method == 'POST':
        username = request.form['fname']
        password = request.form['fpwd']

        if authenticate_user(username, password):
            # Authentication successful
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('RootPage'))
        else:
            error = "Invalid username or password."

    return render_template('Login.html', headerTitle="Login", register=True, error=error)






@app.route('/register', methods=['GET', 'POST'])
def RegisterPage():
    
    if request.method == 'GET':
        return render_template('Login.html', headerTitle="Register", register=False)
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
            return render_template('Login.html', headerTitle="Register", register=False)



app.run(host = '0.0.0.0', port = 8080)