import requests
import json
import time
import random

# Replace YOUR_PUBLIC_KEY and YOUR_PRIVATE_KEY with your actual keys
public_key = '991c78bc0acf137f83ad043f0aeb822d'
private_key = '60a6fe79d247f12ada1675482e80d2aebfd08557'

# Helper function to generate the API hash
def generate_hash(ts):
    import hashlib
    hash_input = ts + private_key + public_key
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()

# Function to get information about a character
def get_character_info(name):
    base_url = 'https://gateway.marvel.com/v1/public/characters'
    ts = str(time.time())
    api_hash = generate_hash(ts)
    params = {'ts': ts, 'apikey': public_key, 'hash': api_hash, 'name': name}
    response = requests.get(base_url, params=params)
    data = json.loads(response.text)
    if data['code'] == 200:
        results = data['data']['results']
        if len(results) > 0:
            result = results[0]
            output = {
                'name': result['name'],
                'description': result['description'],
                'thumbnail': result['thumbnail']['path'] + '.' + result['thumbnail']['extension']
            }
            return output
    return None

# Function to get information about a series
def get_series_info(title):
    base_url = 'https://gateway.marvel.com/v1/public/series'
    ts = str(time.time())
    api_hash = generate_hash(ts)
    params = {'ts': ts, 'apikey': public_key, 'hash': api_hash, 'title': title}
    response = requests.get(base_url, params=params)
    data = json.loads(response.text)
    if data['code'] == 200:
        results = data['data']['results']
        if len(results) > 0:
            result = results[0]
            output = {
                'title': result['title'],
                'description': result['description'],
                'thumbnail': result['thumbnail']['path'] + '.' + result['thumbnail']['extension']
            }
            return output
    return None

# Function to get information about a movie
def get_movie_info(title):
    base_url = 'https://www.omdbapi.com/'
    api_key = 'faf7e5bb'
    params = {'apikey': api_key, 't': title, 'plot': 'full'}
    response = requests.get(base_url, params=params)
    data = json.loads(response.text)
    if data['Response'] == 'True':
        output = {
            'title': data['Title'],
            'description': data['Plot'],
            'poster': data['Poster'],
            'rating': data['imdbRating']
        }
        return output
    return None

# Function to generate a response based on the user input
def generate_response(input_text):
    input_text = input_text.lower()
    response = ''
    
    # Check for greetings
    if 'hi' in input_text or 'hello' in input_text:
        response = random.choice(['Hello there!', 'Hi!', 'Hey!'])
    
    # Check for character requests
    elif 'who is' in input_text or 'tell me about' in input_text:
        name = input_text.replace('who is', '').replace('tell me about', '').strip()
        info = get_character_info(name)
        if info:
            response = info['name'] + ' is ' + info['description'] + '. Here\'s a picture: ' + info['thumbnail']
        else:
            response = "Sorry man I ain't got that{name}."
    
    # Check for movie requests
    elif 'movie' in input_text or 'film' in input_text:
        title = input_text.replace('movie', '').replace('film', '').strip()
        info = get_movie_info(title)
        if info:
            response = f"{info['title']} is a movie with a rating of {info['rating']}. Here's a poster: {info['poster']}"
        else:
            response = f"Sorry, I couldn't find information about {title}."
    
    # Check for series requests
    elif 'series' in input_text:
        title = input_text.replace('series', '').strip()
        info = get_series_info(title)
        if info:
            response = f"{info['title']} is a series. Here's a picture: {info['thumbnail']}"
        else:
            response = f"Sorry, I couldn't find information about {title}."
    
    # If no match found, ask for clarification
    else:
        response = "I'm sorry, I didn't understand your request. Can you please rephrase?"
        
    return response

