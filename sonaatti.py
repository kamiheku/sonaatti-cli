#!/usr/bin/env python

"""
sonaatti.py
Usage: sonaatti.py RESTAURANT
Fetches the menu for a given Sonaatti student restaurant from sonaatti.fi.
"""

from bs4 import BeautifulSoup
import requests
import re
import click

# A listing of the restaurants with their corresponding URL's
restaurants = {'lozzi':       'http://www.sonaatti.fi/lozzi/',
               'syke':        'http://www.sonaatti.fi/syke/',
               'tilia':       'http://www.sonaatti.fi/ravintola_t/',
               'kvarkki':     'http://www.sonaatti.fi/kvarkki/',
               'ylisto':      'http://www.sonaatti.fi/ylisto/',
               'piato':       'http://www.sonaatti.fi/piato/',
               'wilhelmiina': 'http://www.sonaatti.fi/wilhelmiina/',
               'uno':         'http://www.sonaatti.fi/uno/'}

def cleanup(food):
    """Removes unnecessary tags and whitespace from a 'foodstring'
    
    Args:
        food (str): The string to be cleaned up
    
    Returns:
        str: A cleaned up string
    """
    # Removes dietary tags such as #VL, #G etc.
    food = re.sub("#[\S]* *", " ", food)
    # Replaces multiple spaces with a single one
    food = re.sub("  +", " ", food)
    food = food.strip()
    return food

def getHtmlData(restaurant):
    """Gets the data from the restaurant's site.

    Args:
        restaurant (str): The name of the restaurant

    Returns:
        str: The HTML of the site
    """
    url = restaurants[restaurant]
    r = requests.get(url)
    htmldata = r.text
    return htmldata

@click.command()
@click.argument('restaurant')
def getFoods(restaurant):
    """Prints the menu for a given restaurant.
    Args:
        restaurant (str): The name of the restaurant
    """
    htmldata = getHtmlData(restaurant)
    soup = BeautifulSoup(htmldata, "html.parser")
    foods = soup.find(class_='ruuat')
    foods = foods.find_all('p')
    foods = list(map(lambda x: x.string, foods))
    foods = filter(None, foods)
    foods = list(map(cleanup, foods))
    for food in foods:
        print(food)

if __name__ == "__main__":
    getFoods()
