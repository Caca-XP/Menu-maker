import pandas as pd
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
import json
import os

# TODO Generelise the code to allow for more than 2 items per day
# TODO be able to have different number of items per day
# TODO make any pemanent menu items
# TODO Generelise the spreadsheet to allow someone other than me to use it
# TODO Use weather data scraped from the internet to generate the weather and temperature
# TODO Make a GUI for the app, sources = https://realpython.com/django-todo-lists/
# TODO Make a method to add new dishes data to the spreadsheet
# TODO More Ideas on what to add from spreadsheet
# TODO Add documentation to the code
# TODO make an option to print out the list of ingredients needed for the week
# TODO make an option to print out the list of ingredients needed for the day
# TODO maybe make a connection to grocer.nz?


# _____________Settings_____________
# TODO testing settings
# TODO maybe make sure the input type is correct
# TODO make sure the num_items is the same number as len(names_of_items) and vice versa
# TODO make a class for settings and store each prompt in a variable so that it's easier to change

def set_settings():
    num_items = int(input("Enter the number of items per day: "))
    names_of_items = input("Enter the names of the items: (comma separated \", \") ").split(", ")
    days = input("Enter the days of the week: (comma separated \", \") ").split(", ")
        
    # permantent example: "Spaghetti, Monday:1, Tuesday:2|Soup, Wednesday:1"
    permanent = input("Enter the permanent items with the format: Dish, Day:time, Day:time|Dish, Day:time, etc\nTime = " + str(range(1, num_items)) +"\nDays = "+ str(days) +"\n").split("|")
    # reformats the permanent items into a dictionary
    permanent_dict = {}
    for item in permanent:
        day_time = item.split(", ")
        time_dict = {}
        for day in day_time[1:]:
            time_dict[day.split(":")[0]] = day.split(":")[1]
        permanent_dict[day_time[0]] = time_dict
    weather_source = input("Enter the weather source: (comma separated \", \")").split(", ")
    # TODO make more prompts for the settings(OR do it when there's GUI)
    
    setting = {
        "Number of Items" : num_items,
        "Names of Items" : names_of_items,
        "Days" : days,
        "Permanent Items" : permanent_dict,
        "Weather" : weather_source,
        "GUI" : False,
        "csv" : "Menu.csv",
    }
    myJSON = json.dumps(setting, indent=4)

    with open("settings.json", "w") as jsonfile:
        jsonfile.write(myJSON)
        print("Write successful")
        jsonfile.close()
        
def get_settings():
    with open("settings.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        return data
    
def change_settings():
    # print the whole settings.json
    # ask which setting to change
    # change the setting
    # save the settings.json
    # ask if want to change more settings
    # if yes, repeat
    # if no, exit
    print("Change settings")
    settings = get_settings()
    print(settings)
    while True:
        setting = input("Which setting do you want to change? ")
        if setting in settings.keys():
            settings[setting] = input("What do you want to change it to? ")
        else:
            print("Invalid setting")
        repeat = input("Do you want to change more settings? ")
        if repeat not in ['yes', 'Yes', 'y', 'Y']:
            break
    with open("settings.json", "w") as jsonfile:
        myJSON = json.dump(settings, jsonfile, indent=4)
        print("Change successful")
        jsonfile.close()
    

def default_settings():
    # delete settings.json
    # make a new settings.json with default settings
    file_path = "settings.json"
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Setting back to default")
    default = {
        "Number of Items" : 2,
        "Names of Items" : ["Item 1", "Item 2"],
        "Days" : ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        "Permanent Items" : {},
        "Weather" : ["clear", "cloudy", "rain", "thunderstorm", "mild showers"],
        "GUI" : False,
        "csv" : "Menu.csv",
    }
    myJSON = json.dumps(default, indent=4)

    with open("settings.json", "w") as jsonfile:
        jsonfile.write(myJSON)
        print("Write successful")

if not os.path.exists("settings.json"):
    default = input("Do you want to use the default settings? ")
    if default in ['yes', 'Yes', 'y', 'Y']:
        default_settings()
    else:
        set_settings()
    change = input("Do you want to change the settings? ")
    if change in ['yes', 'Yes', 'y', 'Y']: 
        change_settings()

settings = get_settings()
num_items = settings["Number of Items"]
names_of_items = settings["Names of Items"]
days_set = settings["Days"]
permanent = settings["Permanent Items"]
weather_set = settings["Weather"]
csv = settings["csv"]


def plot_freq(menu):
    dishes = menu['Dish'].unique()
    fig,axes = plt.subplots(ncols=num_items)
    freq = pd.DataFrame(index=dishes,columns=['Frequency'])
    for dish in dishes:
        freq.loc[dish]['Frequency'] = len(menu[menu['Dish'] == dish])

    freq[freq['Frequency']>1].plot(kind='barh', ax=axes[0])
    freq[freq['Frequency']==1].plot(kind='barh', figsize=(10,17), ax=axes[1])
    plt.title('Frequency of Dishes')
    plt.xlabel('Frequency')
    fig.tight_layout()
    plt.show()

# make a plot on the rating of the dishes
def plot_rating(menu):
    dishes = menu['Dish'].unique()
    pd.to_numeric(menu['Rating (Subjective to caca)'])
    fig,axes = plt.subplots(ncols=num_items)
    rate = pd.DataFrame(index=dishes,columns=['Rating'])
    for dish in dishes:
        rate.loc[dish]['Rating'] = menu[menu['Dish'] == dish]['Rating (Subjective to caca)'].mean()
    rate.sort_values(by='Rating', ascending=False, inplace=True)
    rate[rate['Rating']>=8].plot(kind='barh', ax=axes[0], xlim=(7,11))
    rate[rate['Rating']<8].plot(kind='barh', figsize=(10,17), ax=axes[1], xlim=(3,8))
    plt.title('Rating of Dishes')
    plt.xlabel('Rating')
    fig.tight_layout()
    plt.show()

def print_weekly(week):
    for day in week.index:
        print(day)
        for t in names_of_items:
            print(t+': '+ str(week.loc[day][t]))
        print()
        
def make_menu(menu, weather):
    rng = rand.default_rng()
    days = days_set
    week = pd.DataFrame(index=days, columns=names_of_items)
    weeknull = week.isnull()
    for day in days:
        for t in names_of_items:
            # check if the item already exists, if not, generate a new one
            if weeknull.loc[day][t] == False:
                continue
            w = weather.loc[day][t]
            menuW = menu[menu['Weather'] == w]
            while True:
                num = rng.integers(0, len(menu))
                # check if the menu is in the correct weather and has a rating of 6 or above
                if menu.loc[num]['Dish'] not in menuW['Dish'].values or int(menu.loc[num]['Rating (Subjective to caca)']) <= 6:
                    continue
                if menu.loc[num]['Dish'] not in permanent.keys():
                    week.loc[day][t] = menu.loc[num]['Dish']
                    weeknull = week.isnull()
                    break
    print(week)
    return week

def change_df1(week):
    day = ""
    while True:
        day = input('Which day do you want to change? ')
        if day in week.index:
            break
    item = input('What item do you want to change to? ')
    while True:
        time = input('Which time do you want to change? ' + str(names_of_items) + ' ')
        if time in names_of_items:
            break
    confirmation = input('Are you sure you want to change '+week.loc[day][time]+' to '+item+'? ')
    if confirmation in ['yes', 'Yes', 'y', 'Y']:
        week.loc[day][time] = item
    print(week)
    return week

def change_df(week, allowed):
    day = ""
    while True:
        day = input('Which day do you want to change? ')
        if day in week.index:
            break
    while True:
        item = input('What item do you want to change to? ')
        if item in allowed:
            break
    while True:
        time = input('Which time do you want to change? ' + str(names_of_items) + ' ')
        if time in names_of_items:
            break
    confirmation = input('Are you sure you want to change '+week.loc[day][time]+' to '+item+'? ')
    if confirmation in ['yes', 'Yes', 'y', 'Y']:
        week.loc[day][time] = item
    print(week)
    return week

def repeat_changes(week, name):
    change = input('Do you want to make changes to the '+ name +'? ')
    if change not in ['yes', 'Yes', 'y', 'Y']:
        return week
    while True:
        if name == 'weather':
            week = change_df(week, weather_set)
        else:
            week = change_df1(week)
        repeat = input('Do you want to make more changes? ')
        if repeat not in ['yes', 'Yes', 'y', 'Y']:
            break
    return week

def make_weather():
    days = days_set
    weather = pd.DataFrame(index=days, columns=names_of_items)
    weather_abrev = []
    for weather_type in weather_set:
        # the first letter of each weather type
        # if already in the list, go to the next alphabet
        if weather_type[0] in weather_abrev:
            for i in range(97, 123):
                if chr(i) not in weather_abrev:
                    weather_abrev.append(chr(i))
                    break
        else:
            weather_abrev.append(weather_type[0])
    print(weather_abrev)
    
    for day in days:
        while True:
            w = input('What is the weather like on '+day+'?' + str(weather_abrev) + ' for ' + str(weather_set) + ' \n')
            if w in weather_abrev or w in weather_set:
                break
        if w in weather_abrev:
            w = weather_set[weather_abrev.index(w)]
        
        for t in names_of_items:
            weather.loc[day][t] = w
    print(weather)
    weather = repeat_changes(weather, 'weather')
    return weather

def ask_for_retry():
    retry = input('Do you want to try again? ')
    if retry in ['yes', 'Yes', 'y', 'Y']:
        return True
    return False

# if there's no setting config file, make one
# if there is, read the config file
# make an option to change the config file




menuOri = pd.read_csv(csv)
# plot_freq(menuOri)
# plot_rating(menuOri)

weather = make_weather()
weekMenu = make_menu(menuOri, weather)
weekMenu = repeat_changes(weekMenu, 'menu')
while True:
    if ask_for_retry():
        weekMenu = make_menu(menuOri, weather)
    else:
        break
print_weekly(weekMenu)




