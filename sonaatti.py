#!/usr/bin/env python3

"""
sonaatti.py
Usage: sonaatti.py RESTAURANT
Fetches the menu for a given Sonaatti student restaurant from sonaatti.fi.
"""

import urllib.request
import time
import json
import click
from sys import exit
from datetime import date
from collections import OrderedDict

RESTAURANT_IDS = { 
    "libri" : "137814",
    "lozzi" : "137828",
    "syke" : "137833",
    "tilia" : "137838",
    "kvarkki" : "137876",
    "ylisto" : "137871",
    "piato" : "110874",
    "wilhelmiina" : "137866",
    "uno" : "137861",
    "normaalikoulu" : "138323",
    "novelli" : "137881"
}

API_URL = "http://www.sonaatti.fi/api/restaurant/menu/week?language=fi&restaurantPageId={}&weekDate={}"
TODAY = date.today().strftime("%-d.%-m.%Y")

def getdata(restaurant):
    """Gets JSON for the specified restaurant and converts to dict

    Args:
        restaurant (str): Name of the restaurant to fetch the data for

    Returns:
        dict: The JSON, dictified
    """
    today_dash = date.today().strftime("%Y-%-m-%-d")
    try:
        data = json.loads(
            urllib.request.urlopen(
                API_URL.format(RESTAURANT_IDS[restaurant], today_dash)
            ).read())
        return data
    except:
        print("Couldn't fetch data for restaurant :(")
        exit(1)

def parsedata(data):
    """Parses a dict containing the data for a restaurant, out comes an
    OrderedDict with lunches/meals

    Args:
        data (dict): Data for a restaurant

    Returns:
        OrderedDict: OrderedDict with lunches/meals
    """
    lunches = OrderedDict()

    for day in data['LunchMenus']:
        if day['Date'] == TODAY:
            for lunch in day['SetMenus']:
                if lunch['Name'] != None:
                    lunch_name = lunch['Name']
                    if lunch_name not in lunches.keys():
                        lunches[lunch_name] = []
                    for meal in lunch['Meals']:
                        lunches[lunch_name].append(meal['Name'])
            break

    return lunches

def printdata(lunches):
    """Prettyprints the given lunch data

    Args:
        lunches (OrderedDict): OrderedDict with lunches/meals

    Returns:
        None
    """
    for lunch in lunches.keys():
        print(lunch.title())
        for meal in (lunches[lunch]):
            print(" " * 4 + meal)

@click.command()
@click.argument('restaurant')
def getandprint(restaurant):
    restaurant = restaurant.lower()
    if restaurant not in RESTAURANT_IDS.keys():
        print('Restaurant "{}" not found. Valid restaurants:'.format(restaurant))
        for r in RESTAURANT_IDS.keys():
            print(r.title())
        exit(1)

    data = getdata(restaurant)
    lunches = parsedata(data)

    print(restaurant.title() + '\n')
    printdata(lunches)

if __name__ == "__main__":
    getandprint()
