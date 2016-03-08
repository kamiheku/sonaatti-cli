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

def cleanup(dish):
    """Removes unnecessary tags and whitespace from a 'dishstring'
    
    Args:
        dish (str): The string to be cleaned up
    
    Returns:
        str: A cleaned up string
    """
    # Removes dietary tags such as #VL, #G etc.
    dish = re.sub("#[\S]* *", " ", dish)
    # Replaces multiple spaces with a single one
    dish = re.sub("  +", " ", dish)
    dish = dish.strip()
    return dish

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
def getDishes(restaurant):
    """Prints the menu for a given restaurant.
    Args:
        restaurant (str): The name of the restaurant
    """
    htmldata = getHtmlData(restaurant)
    soup = BeautifulSoup(htmldata, "html.parser")
    dishes = soup.find(class_='ruuat')
    dishes = dishes.find_all('p')
    dishes = list(map(lambda x: x.string, dishes))
    dishes = filter(None, dishes)
    dishes = list(map(cleanup, dishes))
    for dish in dishes:
        print(dish)

if __name__ == "__main__":
    getDishes()
