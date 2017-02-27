#!/usr/bin/env python3

import urllib.request
import time
import json
from datetime import date

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

today_dash = date.today().strftime("%Y-%-m-%-d")
today_period = date.today().strftime("%-d.%-m.%Y")
data = json.loads(urllib.request.urlopen("http://www.sonaatti.fi/api/restaurant/menu/week?language=fi&restaurantPageId={}&weekDate={}".format(RESTAURANT_IDS['piato'], today_dash)).read())

for day in data['LunchMenus']:
    if day['Date'] == today_period:
        for lunch in day['SetMenus']:
            if lunch['Name'] != None:
                print(lunch['Name'])
                for meal in lunch['Meals']:
                    print(" "*4 + meal['Name'])
    break
