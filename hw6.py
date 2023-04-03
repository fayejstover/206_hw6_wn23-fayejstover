import requests
import json
import unittest
import os
import math

###########################################
# Your name: # Faye Stover
# Who you worked with: # 
###########################################

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
    except FileNotFoundError:
        data = {}
        
    return data
    
    '''
Loads a JSON cache from filename if it exists
Parameters
----------
filename: string
the name of the cache file to read in
Returns
-------
dict
if the cache exists, a dict with loaded data
if the cache does not exist, an empty dict
    '''

pass


def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)
    
    '''
Encodes dict into JSON format and writes
the JSON to filename to save the search results
Parameters
----------
filename: string
the name of the file to write a cache to
dict: cache dictionary
Returns
-------
None
does not return anything
    '''

pass


def get_swapi_info(url, params=None):
    cache_dict = load_json("swapi_cache.json")

    # Check if data already exists in cache
    if url in cache_dict:
        print(f"Retrieving {url} from cache...")
        return cache_dict[url]

    # If the page number does not exist in the dictionary, it makes a request
    print(f"Requesting {url} from API...")
    response = requests.get(url, params=params)

    # Check if API request was successful
    if response.status_code == 200:
        data = response.json()
        
        cache_dict[url] = data
        write_json("swapi_cache.json", cache_dict)

        return data
    
    else:
        # if API request was not successful
        print(f"Request for {url} failed with status code {response.status_code}")
        return None
    
    '''
1. Checks if the page number is found in the dict return by `load_json`
2. If the page number does not exist in the dictionary, it makes a request
(using get_swapi_info)
3. Add the data to the dictionary (the key is the page number (Ex: page 1) and
the value is the results).
4. Write out the dictionary to a file using write_json.
Parameters
----------
people_url (str): a url that provides information about the
characters in the Star Wars universe (https://swapi.dev/api/people).
filename(str): the name of the file to write a cache to
'''

pass


def cache_all_pages(people_url, filename):
    if load_json(filename):
        cache_dct = load_json(filename)
    else:
        cache_dct = {}
    
    newdct = {}

    for i in range(10):
        page = cache_dct.get(str(i), get_swapi_info(people_url))
        results = page.get('results')
        cache_dct["page " + str(i+1)] = results
    
    # Write out the dictionary to a file using write_json.
    write_json(filename, cache_dct)




    '''
 1. Checks if the page number is found in the dict return by `load_json`
 2. If the page number does not exist in the dictionary, it makes a request
 (using get_swapi_info)
 3. Add the data to the dictionary (the key is the page number (Ex: page 1) and
 the value is the results).
 4. Write out the dictionary to a file using write_json.
 Parameters
 ----------
 people_url (str): a url that provides information about the
 characters in the Star Wars universe (https://swapi.dev/api/people).
 filename(str): the name of the file to write a cache to
    '''
    
    pass

def get_starships(filename):
    cache_dict = load_json(filename)
    if not cache_dict:
        cache_dict = {}

    # Get data for each character
    characters_url = 'https://swapi.dev/api/people/'
    character_data = []

    while characters_url:
        response = requests.get(characters_url)
        if response.status_code == 200:
            data = response.json()
            character_data.extend(data['results'])
            characters_url = data['next']

    starships_dict = {}

    for character in character_data:
        name = character['name']
        starships = []

        # Loop over all starship URLs for the character / check if starship data is already in cache
        for starship_url in character['starships']:
            if starship_url in cache_dict:
                starship_data = cache_dict[starship_url]
            else:
                starship_data = get_swapi_info(starship_url)
                cache_dict[starship_url] = starship_data
                write_json(filename, cache_dict)

            starships.append(starship_data['name'])

        if starships:
            starships_dict[name] = starships

    return starships_dict

    
    '''
Access the starships url for each character (if any) and pass it to the
get_swapi_info function
to get data about a person's starship.
Parameter
----------
filename(str): the name of the cache file to read in
Returns
-------
dict: dictionary with the character's name as a key and a list of the name
their
starships as the value
    '''
    
pass

#################### EXTRA CREDIT ######################

def calculate_bmi(filename):

    base_url = 'https://swapi.dev/api/people/'
    bmi_dict = {}
    cache_dict = load_json(filename)
    
    if not cache_dict:
        cache_dict = {}

    while base_url and len(bmi_dict) < 59:
        response = requests.get(base_url)
        data = response.json()

        for character in data['results']:
            name = character['name']
            height = character['height']
            mass = character['mass']

            if height.isnumeric() and mass.isnumeric():
                height_m = int(height) / 100
                mass_kg = int(mass)
                bmi = round(mass_kg / (height_m ** 2), 2)
                bmi_dict[name] = bmi

            if name not in cache_dict:
                cache_dict[name] = {'height': height, 'mass': mass}

            if len(bmi_dict) == 59:
                break

        base_url = data['next']

    write_json(filename, cache_dict)
    return bmi_dict



'''
Calculate each character's Body Mass Index (BMI) if their height and mass is
known. With the metric
system, the formula for BMI is weight in kilograms divided by height in meters
squared.

Since height is commonly measured in centimeters, an alternate calculation
formula,
dividing the weight in kilograms by the height in centimeters squared, and then
multiplying
the result by 10,000, can be used.
Parameter
----------
filename(str): the name of the cache file to read in
Returns
-------
dict: dictionary with the name as a key and the BMI as the value
'''

pass

class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.filename = dir_path + '/' + "swapi_people.json"
        self.cache = load_json(self.filename)
        self.url = "https://swapi.dev/api/people"
    
    def test_write_json(self):
        write_json(self.filename, self.cache)
        dict1 = load_json(self.filename)
        self.assertEqual(dict1, self.cache)
    
    def test_get_swapi_info(self):
        people = get_swapi_info(self.url)
        tie_ln = get_swapi_info("https://swapi.dev/api/vehicles", {"search": "tie/ln"})
        self.assertEqual(type(people), dict)
        self.assertEqual(tie_ln['results'][0]["name"], "TIE/LN starfighter")
        self.assertEqual(get_swapi_info("https://swapi.dev/api/pele"), None)

    def test_cache_all_pages(self):
        cache_all_pages(self.url, self.filename)
        swapi_people = load_json(self.filename)
        print("swapi_people: ")
        print(swapi_people)
        self.assertEqual(type(swapi_people['page 1']), list)
    
    def test_get_starships(self):
        starships = get_starships(self.filename)
        self.assertEqual(len(starships), 19)
        self.assertEqual(type(starships["Luke Skywalker"]), list)
        self.assertEqual(starships['Biggs Darklighter'][0], 'X-wing')

    def test_calculate_bmi(self):
        bmi = calculate_bmi(self.filename)
        self.assertEqual(len(bmi), 56)
        self.assertAlmostEqual(bmi['Greedo'], 24.73)

if __name__ == "__main__":
    unittest.main(verbosity=2) 