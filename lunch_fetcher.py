import json
import requests
import datetime
import random

HERZI = "https://www.sodexo.fi/ruokalistat/output/weekly_json/111"
REAKTORI = "https://www.foodandco.fi/modules/json/json/Index?costNumber=0812&language=fi"
NEWTON = "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/93077/6?lang=fi"

RESTAURANTS = [HERZI, REAKTORI, NEWTON]


def is_today_finnish_weekday(weekday):
    weekdays = "Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"
    weekday_today = datetime.datetime.today().weekday()

    if weekday == weekdays[weekday_today]:
        return True
    else:
        return False



def reaktori():
    """ Fetches the lunch data from a json

    Returns
    -------
    list
        list of food components
    """
    # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")

    # open json file
    response = requests.get(REAKTORI)
    lunch_json = json.loads(response.text)
    
    # navigate the json
    menus = lunch_json["MenusForDays"]
    for day in menus:
        if day["Date"][0:10] == today:
            try:
             return day["SetMenus"][2]["Components"]
            except IndexError:
                # default to saying someone ate the food if the restaurant has no food
                victims = ["Otso", "Eemeli", "Nokia", "Joonas", "Murinabot", "Elias"]
                components = [f"{random.choice(victims)} söi kaiken :("]
                return components


def newton():
    """Fetches the lunch data from a json

    Returns
    -------
    list
        list of food components
    """
    # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # open json file
    response = requests.get(NEWTON)
    lunch_json = json.loads(response.text)
    
    # default to saying someone ate the food if the restaurant has no food
    victims = ["Otso", "Eemeli", "Nokia", "Joonas", "Murinabot", "Elias"]
    components = [f"{random.choice(victims)} söi kaiken :("]

    # navigate the json
    try:
        days = lunch_json[0]["menuTypes"][2]["menus"][0]["days"]
    except IndexError:
        return components

    components = []    
    for day in days:
        if str(day["date"]) == today:
            items = day["mealoptions"][0]["menuItems"]

            for item in items:
                components.append(item["name"])
            
            if len(day["mealoptions"]) == 2:
                items = items = day["mealoptions"][1]["menuItems"]
                for item in items:
                    components.append(item["name"])
    
    print(components)
    return components

def soos():
    # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # open json file
    response = requests.get(NEWTON)
    lunch_json = json.loads(response.text)

    # default to saying someone ate the food if the restaurant has no food
    victims = ["Otso", "Eemeli", "Nokia", "Joonas", "Murinabot", "Elias"]
    components = [f"{random.choice(victims)} söi kaiken :("]

    # navigate the json
    try:
        days = lunch_json[0]["menuTypes"][1]["menus"][0]["days"]
    except IndexError:
        return components

  
    for day in days:
        if str(day["date"]) == today:

            for menu in day["mealoptions"]:
                name = menu["name"]
                if name == "SÅÅS BAR":
                    components = []
                    for item in menu["MenuItems"]:
                        components.append(item["name"])
                    break

    return components

def hertsi():
     # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # open json file
    response = requests.get(HERZI)
    lunch_json = json.loads(response.text)

    # default to saying someone ate the food if the restaurant has no food
    victims = ["Otso", "Eemeli", "Nokia", "Joonas", "Murinabot", "Elias"]
    components = [f"{random.choice(victims)} söi kaiken :("]

    # navigate json
    for day in lunch_json["mealdates"]:
        if is_today_finnish_weekday(day["date"]):
            components = []
            courses = day["courses"]
            for course in courses:
                # I have no idea why the fuck I need to do this but here we are
                course1 = courses[course]
                components.append(course1["title_fi"])
    
    return components


def get_lists():
    """Returns a dictionary of restaurants food lists

    Returns
    -------
    dict
        dictionary of restaurant menus
    """
    return {"Reaktori" : reaktori(), "Newton" : newton(), "Såås bar" : soos(), "Hertsi" : hertsi()}
