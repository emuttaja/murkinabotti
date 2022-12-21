import json
import requests
import datetime
import random

HERZI = "https://www.sodexo.fi/ruokalistat/output/weekly_json/111"
REAKTORI = "https://www.compass-group.fi/menuapi/feed/json?costNumber=0812&language=fi"
NEWTON = "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/93077/6?lang=fi"

VICTIMS = ["Eemeli", "Nokia", "Otso", "Joonas", "Lauri", "Elias",
           "Aleksi", "Pekka", "Lauri", "Murinabot"]

RESTAURANTS = [HERZI, REAKTORI, NEWTON]


def is_today_finnish_weekday(weekday):
    weekdays = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
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
    components = []
    menus = lunch_json["MenusForDays"]
    for day in menus:
        if day["Date"][0:10] == today:
            try:
                for option in day["SetMenus"]:
                    if option["Name"] == "Lounas":
                        if option["Components"] == []:
                            continue
                        else:
                            for component in option["Components"]:
                                flag = True
                                i = 0
                                while flag:
                                    if component[i] == "(":
                                        flag = False
                                    elif i == len(component):
                                        flag = False
                                    i = i + 1
                                components.append(component[:i - 1])
                
                print(components)
                return components

                # return day["SetMenus"][2]["Components"]
            except IndexError:
                # default to saying someone ate the food if the restaurant has no food
                components = [f"{random.choice(VICTIMS)} söi kaiken :("]
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
    components = [f"{random.choice(VICTIMS)} söi kaiken :("]

    # navigate the json
    try:
        days = lunch_json[0]["menuTypes"][1]["menus"][0]["days"]
    except IndexError:
        return components

    components = []    
    for day in days:
        if str(day["date"]) == today:
            #items = day["mealoptions"][0]["menuItems"]

            for meal_option in day["mealoptions"]:
                for item in meal_option["menuItems"]:
                    components.append(item["name"])
    
    return components


def soos():
    # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # open json file
    response = requests.get(NEWTON)
    lunch_json = json.loads(response.text)

    # default to saying someone ate the food if the restaurant has no food
    components = [f"{random.choice(VICTIMS)} söi kaiken :("]

    # navigate the json
    try:
        days = lunch_json[0]["menuTypes"][4]["menus"][0]["days"]
    except IndexError:
        return components

  
    for day in days:
        if str(day["date"]) == today:

            for menu in day["mealoptions"]:
                name = menu["name"]
                if name == "SÅÅS BAR":
                    components = []
                    for item in menu["menuItems"]:
                        components.append(item["name"])
                    break

    return components


def fusion_meal():
    # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # open json file
    response = requests.get(NEWTON)
    lunch_json = json.loads(response.text)

    # default to saying someone ate the food if the restaurant has no food
    components = [f"{random.choice(VICTIMS)} söi kaiken :("]

    # navigate the json
    try:
        days = lunch_json[0]["menuTypes"][4]["menus"][0]["days"]
    except IndexError:
        return components

  
    for day in days:
        if str(day["date"]) == today:

            for menu in day["mealoptions"]:
                name = menu["name"]
                if name == "FUSION MEAL":
                    components = []
                    for item in menu["menuItems"]:
                        components.append(item["name"])
                    break

    return components

def fusion_burger():
    # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # open json file
    response = requests.get(NEWTON)
    lunch_json = json.loads(response.text)

    # default to saying someone ate the food if the restaurant has no food
    components = [f"{random.choice(VICTIMS)} söi kaiken :("]

    # navigate the json
    try:
        days = lunch_json[0]["menuTypes"][4]["menus"][0]["days"]
    except IndexError:
        return components

  
    for day in days:
        if str(day["date"]) == today:
            print("wtf - day found")
            print(day["mealoptions"])
            for menu in day["mealoptions"]:
                name = menu["name"]
                print(name)
                if name == "FUSION BURGER":
                    components = []
                    for item in menu["menuItems"]:
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
    components = [f"{random.choice(VICTIMS)} söi kaiken :("]

    # navigate json
    for day in lunch_json["mealdates"]:
        if is_today_finnish_weekday(day["date"]):
            components = []
            courses = day["courses"]
            for course in courses:
                course1 = courses[course]
                components.append(course1["title_fi"])
    
    return components


def fusion():
    # get current date
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # open json file
    response = requests.get(NEWTON)
    lunch_json = json.loads(response.text)

    # default to saying someone ate the food if the restaurant has no food
    components = [f"{random.choice(VICTIMS)} söi kaiken :("]

    # navigate the json
    try:
        days = lunch_json[0]["menuTypes"][4]["menus"][0]["days"]
    except IndexError:
        return components

  
    for day in days:
        if str(day["date"]) == today:
            for menu in day["mealoptions"]:
                name = menu["name"]
                if name == "FUSION":
                    components = []
                    for item in menu["menuItems"]:
                        components.append(item["name"])
                    break

    return components

def get_lists():
    """Returns a dictionary of restaurants food lists

    Returns
    -------
    dict
        dictionary of restaurant menus
    """
    if (is_today_finnish_weekday("Perjantai")):
        return {
            "Newton" : newton(),  
            "Hertsi" : hertsi(),
            "Siipeä": fusion(),
            "Reaktori" : reaktori(), 
        }

    return {
            "Newton" : newton(),  
            "Hertsi" : hertsi(),
            "Fusion Meal": fusion_meal(),
            "Reaktori" : reaktori(), 
            "Fusion Burger" : fusion_burger(),
            "Såås bar" : soos(),
            }
