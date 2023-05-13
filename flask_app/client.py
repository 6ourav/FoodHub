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
        self.host = 'BEXoRr0ICXnYgnj5wT3GY8rVim9shFz1N9ciLZJAfednLHF9GsQ28AwJtdd5StCIwA9bHYbzq2-ORcobWXOuXKzkHnBDdni_O3loOxZVk1vpdfE-6C3YRlLY2KZRZHYx'