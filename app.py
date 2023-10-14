#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import os

import pymongo
import datetime
from bson.objectid import ObjectId
import sys


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

# Login
@app.route('/', methods = ['GET', 'POST'])
def LoginPage():
    if (request.method == 'GET'):
        return render_template('base.html', headerTitle = "Login", register = True)
    else: 
        name = request.form['fname']
        pwd = request.form['fpwd']
        if (name == pwd):  # perform validate login info via db !! PLACEHOLDER
            return redirect(url_for('RootPage'))
        else:
            return render_template('base.html', headerTitle = "Login", register = True)
    



# Register
@app.route('/register', methods = ['GET', 'POST'])
def RegisterPage():
    if (request.method == 'GET'):
        return render_template('base.html', headerTitle = "Register", register = False)
    else: 
        name = request.form['fname']
        pwd = request.form['fpwd']
        # add register info to db
        
        # if success -> LoginPage
        if(True):
            return redirect(url_for('RootPage'))
        else:
            return render_template('base.html', headerTitle = "Register", register = False)




app.run(host = '0.0.0.0', port = 8080)