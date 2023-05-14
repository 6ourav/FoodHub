from flask import Flask, render_template, request
from yelpapi import YelpAPI
import requests
import json

# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime

# local
app = Flask(__name__)
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/388JProj"
app.config["SECRET_KEY"] = b"L\x9d\xfcY\xf1`\x91\xeb\\\xba\xf9\xb5\x8a'\x9c\x1f"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

api_key = "BEXoRr0ICXnYgnj5wT3GY8rVim9shFz1N9ciLZJAfednLHF9GsQ28AwJtdd5StCIwA9bHYbzq2-ORcobWXOuXKzkHnBDdni_O3loOxZVk1vpdfE-6C3YRlLY2KZRZHYx"
yelp_api = YelpAPI(api_key)