from flask import Flask, render_template, request
from yelpapi import YelpAPI
import requests
import json
import os

# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from wtforms.validators import ValidationError

from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from . import app, bcrypt, api_key
from .forms import (
    SearchForm,
    RestaurantReviewForm,
    RegistrationForm,
    LoginForm,
    UpdateBioForm,
    UpdateProfilePicForm
)
from .models import User, Review, Following, load_user
from .utils import current_time
from .client import Restaurant

import io
import base64

def render_stars(rating):
    filled_stars = int(rating)
    
    empty_stars = 5 - filled_stars
    return '★' * filled_stars + '☆' * empty_stars


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    location = request.args.get('location')
    headers = {'Authorization': 'Bearer %s' % api_key}
    params = {'location': location, 'categories': 'restaurants'}
    response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
    data = response.json()
    return render_template('restaurants.html', businesses=data['businesses'], render_stars=render_stars)

@app.route('/restaurants/<business_id>', methods=["GET", "POST"])
def restaurant_detail(business_id):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = f'https://api.yelp.com/v3/businesses/{business_id}'
    response = requests.get(url, headers=headers)
    business = response.json()
    form = RestaurantReviewForm()
    if not form.validate_on_submit():
        for error in form.errors.values():
            for e in error:
                flash(e)
      
    if form.validate_on_submit():
        review = Review(
            commenter=current_user,
            comment=form.comment.data,
            date=current_time(),
            id_restaurant=business_id,
            restaurant_name=business.get('name'),
            rating=form.rating.data,
            stars=render_stars(form.rating.data)
        )
        review.save()
        img = form.image.data
        content_type = f'images/{secure_filename(img.filename)[-3:]}'
        review.image.put(img.stream, content_type=content_type)
        review.save()
        bytes_im = io.BytesIO(review.image.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
        review.modify(image_encoded=image)
        review.save()
        return redirect(url_for('restaurant_detail', business_id=business_id))

    reviews = Review.objects(id_restaurant=business_id).order_by('-date')
    average = Review.objects(id_restaurant=business_id).average('rating')
    render_stars(average)
    return render_template('restaurant_detail.html', business=business, form=form, reviews=reviews, average=average, render_stars=render_stars)


@app.route('/restaurants/<business_id>/review', methods=['POST'])
@login_required
def submit_review(business_id):
    form = RestaurantReviewForm()

    if form.validate_on_submit():
        # Get the restaurant details from the API or your data source


        # Create a new review object
        review = Review(
            commenter=current_user,
            comment=form.comment.data,
            date=current_time(),
            id_restaurant=business_id,
            restaurant_name=business.get('name'),
        )
        # Save the review to the database
        review.save()
        img = form.image.data
        content_type = f'images/{secure_filename(img.file)[-3:]}'
        review.image.put(img.stream, content_type=content_type)
        review.save()
        bytes_im = io.BytesIO(current_user.image.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
        review.modify(image_encoded=image)
        review.save()
        return redirect(url_for('restaurant_detail', business_id=business_id))
        # Fetch the reviews for the current restaurant sorted by newest
    reviews = Review.objects(id_restaurant=business_id).order_by('-date')
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = f'https://api.yelp.com/v3/businesses/{business_id}'
    response = requests.get(url, headers=headers)
    business = response.json()
    return render_template("restaurant_detail.html", form=form, business=business, reviews=reviews)
        # Redirect to the restaurant detail page
        

    # If the form is not valid, render the restaurant detail page again




@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.objects(username=username).first()
    if user is not None:
        following_list = Following.objects(user1=user)
        follower_list = Following.objects(user2=user)
        reviews = Review.objects(commenter=user).order_by("-date")
        is_following = Following.objects(user1=str(current_user.id), user2=str(user.id)).first() is not None
        return render_template("profile.html", user=user, reviews=reviews, is_following=is_following,
                               following_list=following_list, follower_list=follower_list)
    else:
        return render_template("profile.html", error_msg="User does not exist")
    

@app.route("/follow/<username>", methods=["GET", "POST"])
@login_required
def follow_user(username):
    user = User.objects(username=username).first()
    following_change = Following(
        user1 = current_user,
        user2 = user,
        date = current_time()
    )
    following_change.save()
    follower_change = Following(
        user1 = user,
        user2 = current_user,
        date = current_time()
    )
    follower_change.save()
    return redirect(url_for('profile', username=username))

@app.route("/unfollow/<username>", methods=["GET", "POST"])
@login_required
def unfollow_user(username):
    user = User.objects(username=username).first()
    Following.objects(user1=current_user, user2=user).first().delete()
    Following.objects(user1=user, user2=current_user).first().delete()
    return redirect(url_for('profile', username=username))
    
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form1 = UpdateBioForm()
    form2 = UpdateProfilePicForm()
    if "submit1" in request.form and form1.validate_on_submit():
        current_user.modify(bio=form1.bio.data)
        current_user.save()
        return redirect(url_for('profile', username=current_user.username))
    if "submit2" in request.form and form2.validate_on_submit():
        img = form2.profile_picture.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'
        if current_user.profile_picture.get() is None:
            current_user.profile_picture.put(img.stream, content_type=content_type)
        else:
            current_user.profile_picture.replace(img.stream, content_type=content_type)
        current_user.save()
        bytes_im = io.BytesIO(current_user.profile_picture.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
        current_user.modify(pic_encoded=image)
        current_user.save()
        return redirect(url_for('profile', username=current_user.username))
    elif "submit2" in request.form and not form2.validate_on_submit():
        for error in form2.errors.values():
            for e in error:
                flash(e)
    return render_template('edit.html', form1=form1, form2=form2)
    
@app.route("/followlist", methods=["GET", "POST"])
@login_required
def followlist():
    follower = Following.objects(user2=current_user.id).order_by('-date')
    following = Following.objects(user1=current_user.id).order_by('-date')
    return render_template('followlist.html', follower=follower, following=following)
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed
        )
        user.save()
        return redirect(url_for('login'))
    else:
        for error in form.errors.values():
            for e in error:
                flash(e)
    return render_template('register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
        else:
            flash('Login attempt failed')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def custom_404(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)