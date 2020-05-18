#--------------------------------------------------------------------------
# Module: __init__.py
# Desc: The flask application package.
#--------------------------------------------------------------------------
from flask import Flask, flash, redirect, render_template, request,session, escape, url_for,jsonify

# Get a reference to the application object
app = Flask(__name__) 

# Load the config settings
app.config.from_object("config.ProductionConfig")

# Set the secret key to some random bytes. 
# Keep this really secret!
# This will be used for web sessions. 
app.secret_key = app.config["SECRET_KEY"]

import FlaskWebProjectIBMi.views
