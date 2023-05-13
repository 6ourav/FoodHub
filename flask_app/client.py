import requests

class Restaurant:
    def __init__(self, id_restaurant, name, locale):
        self.id_restaurant = id_restaurant
        self.name = name
        self.locale = locale
        
    def __repr__(self):
        return f"Restaurant(id_restaurant={self.id_restaurant}, name='{self.name}', locale='{self.locale}')"
    
class MyRestClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.host = 'vJI6eq7oOj9t13m-BN8yVYHYe3mNe3SDY_p-Mu4y_MYEA2cZGq_DQpfbQQmioToXsXTedSO2Nh8wZnRL1RV_487t-qmMDSyJ8p480AhgpbzAv61SaxhJ3IgXq6VRZHYx'