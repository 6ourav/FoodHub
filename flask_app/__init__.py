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
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/final"
app.config["SECRET_KEY"] = b"L\x9d\xfcY\xf1`\x91\xeb\\\xba\xf9\xb5\x8a'\x9c\x1f"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

api_key = "ieCqIDSYqdh2Cmi222wwGVAJYBCCiEa1VHazzL6YvC7_Ex2fUIKWNI4bfO8QLAPpjVE3qjV6zzurSONBaL3QdRitMKqi9m74F910mknmbOc49KE9JWPiRgoUGadRZHYx"
yelp_api = YelpAPI(api_key)