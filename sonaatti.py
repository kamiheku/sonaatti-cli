#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re
import click

restaurants = {'lozzi':       'http://www.sonaatti.fi/lozzi/',
               'syke':        'http://www.sonaatti.fi/syke/',
               'tilia':       'http://www.sonaatti.fi/ravintola_t/',
               'kvarkki':     'http://www.sonaatti.fi/kvarkki/',
               'ylisto':      'http://www.sonaatti.fi/ylisto/',
               'piato':       'http://www.sonaatti.fi/piato/',
               'wilhelmiina': 'http://www.sonaatti.fi/wilhelmiina/',
               'uno':         'http://www.sonaatti.fi/uno/'}

def cleanup(food):
    # Removes dietary tags such as #VL, #G etc.
    food = re.sub("#[\S]* *", " ", food)
    # Replaces multiple spaces with a single one
    food = re.sub("  +", " ", food)
    food = food.strip()
    return food

def getHtmlData(restaurant):
    url = restaurants[restaurant]
    r = requests.get(url)
    htmldata = r.text
    return htmldata

@click.command()
@click.argument('restaurant')
def getFoods(restaurant):
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
