import requests
from bs4 import BeautifulSoup

def get_first_image_url(query):
    # Prepare the Google Images URL
    search_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"

    # Send a GET request to Google Images
    response = requests.get(search_url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first image element
    image_element = soup.find('img')

    # Extract the URL from the image element
    image_url = image_element['src']

    return image_url

# Example usage
search_query = input("Enter your search query: ")
first_image_url = get_first_image_url(search_query)
print("First image URL:", first_image_url)