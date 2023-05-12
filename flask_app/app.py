from flask import Flask, render_template, request, send_from_directory
from yelpapi import YelpAPI
import requests

app = Flask(__name__, static_folder='static')
api_key = "-hRiWcErZsV9imRBP6C_fukk1OrTfZ0aWuK2fjLsv4tLYQCBAWXlIKN6WTocuY2PjLXXyq4g0F4ASuDWdv82VJidAAl35qvygXhmxmzOW-9nSIE1hT6oVQDVzaVRZHYx"
yelp_api = YelpAPI(api_key)

def render_stars(rating):
    filled_stars = int(rating)
    
    empty_stars = 5 - filled_stars
    return '★' * filled_stars + '☆' * empty_stars

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route('/search')
def search():
    api_key = 'vJI6eq7oOj9t13m-BN8yVYHYe3mNe3SDY_p-Mu4y_MYEA2cZGq_DQpfbQQmioToXsXTedSO2Nh8wZnRL1RV_487t-qmMDSyJ8p480AhgpbzAv61SaxhJ3IgXq6VRZHYx'
    location = request.args.get('location')
    headers = {'Authorization': 'Bearer %s' % api_key}
    params = {'location': location, 'categories': 'restaurants'}
    response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
    data = response.json()
    return render_template('restaurant.html', businesses=data['businesses'], render_stars=render_stars)

@app.route('/restaurants/<business_id>')
def restaurant_detail(business_id):
    api_key = 'vJI6eq7oOj9t13m-BN8yVYHYe3mNe3SDY_p-Mu4y_MYEA2cZGq_DQpfbQQmioToXsXTedSO2Nh8wZnRL1RV_487t-qmMDSyJ8p480AhgpbzAv61SaxhJ3IgXq6VRZHYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = f'https://api.yelp.com/v3/businesses/{business_id}'
    response = requests.get(url, headers=headers)
    business = response.json()
    return render_template('restaurant_detail.html', business=business, render_stars=render_stars)