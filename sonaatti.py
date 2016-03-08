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

def stripEmpty(foods):
    while None in foods:
        foods.remove(None)
    return foods

def stripSpecs(food):
    # Let's strip the *'s ("healthy choice")
    food = food.replace("*", "")
    # food = re.sub("  ", " ", food)
    food = food.replace("  ", " ")
    # And the dietary stuff too
    exp = "#[\S]* *"
    food = re.sub(exp, " ", food)
    food = re.sub("  +", " ", food)
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
    foods = stripEmpty(foods)
    foods = list(map(stripSpecs, foods))
    for food in foods:
        print(food)

# def main():
#     getFoods(restaurant)

if __name__ == "__main__":
    getFoods()
