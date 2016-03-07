#!/usr/bin/env python

from bs4 import BeautifulSoup
from sys import argv
import requests
import re

ravintolat = {'lozzi':       'http://www.sonaatti.fi/lozzi/',
              'syke':        'http://www.sonaatti.fi/syke/',
              'tilia':       'http://www.sonaatti.fi/ravintola_t/',
              'kvarkki':     'http://www.sonaatti.fi/kvarkki/',
              'ylisto':      'http://www.sonaatti.fi/ylisto/',
              'piato':       'http://www.sonaatti.fi/piato/',
              'wilhelmiina': 'http://www.sonaatti.fi/wilhelmiina/',
              'uno':         'http://www.sonaatti.fi/uno/'}

def stripEmpty(ruuat):
    while None in ruuat:
        ruuat.remove(None)
    return ruuat

def stripSpecs(ruoka):
    # Let's strip the *'s ("healthy choice")
    ruoka = ruoka.replace("*", "")
    # Random annoying inconcistencies
    ruoka = ruoka.replace("Veg", "")
    # ruoka = re.sub("  ", " ", ruoka)
    ruoka = ruoka.replace("  ", " ")
    # And the dietary stuff too
    exp = "#[A-Z#, ]*( |$)"
    ruoka = re.sub(exp, " ", ruoka)
    ruoka = re.sub("  +", " ", ruoka)
    return ruoka

def getHtmlData(ravintola):
    r = requests.get("http://www.sonaatti.fi/%s/" %ravintola)
    htmldata = r.text
    return htmldata

def getFoods(ravintola):
    htmldata = getHtmlData(ravintola)
    keitto = BeautifulSoup(htmldata, "html.parser")
    ruuat = keitto.find(class_='ruuat')
    ruuat = ruuat.find_all('p')
    ruuat = list(map(lambda x: x.string, ruuat))
    ruuat = stripEmpty(ruuat)
    ruuat = list(map(lambda x: stripSpecs(x), ruuat))
    for ruoka in ruuat:
        print(ruoka)

def main():
    getFoods(argv[-1])

if __name__ == "__main__":
    main()
