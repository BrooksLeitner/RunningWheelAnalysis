import pandas as pd
import math
import numpy as np
import seaborn as sns

def preprocess(data):
    dict_of_cages = dict(iter(data.groupby('Cage')))

    for cage in dict_of_cages:
#convert Time from object to a date/time variable
        dict_of_cages[cage]["Time"] = pd.to_datetime(dict_of_cages[cage]["Time"])

    #convert wheel counts into distance in km
    #Diameter of wheel is 9.2 cm, circumference equals pi*diameter, thus counts*pi*9.2 = distance in cm
    #distance in cm / 100 = distance in meters
        dict_of_cages[cage]["Distance_meters"] = (dict_of_cages[cage]["Wheel (counts)"] * math.pi * 9.2)/100
    #reset the index to the time series
        dict_of_cages[cage] = dict_of_cages[cage].resample('D', on='Time').sum()

    return dict_of_cages


def remove_zeros(dict_of_cages):
    for cage in dict_of_cages:
        dict_of_cages[cage] = dict_of_cages[cage][dict_of_cages[cage]['Distance_meters'] != 0]
    return dict_of_cages


def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list


def assign(dict_of_cages):
    mouse_list = getList(dict_of_cages)
    
    for mouse, key in zip(mouse_list, dict_of_cages.keys()):
        dict_of_cages[key]['Mouse'] = mouse

    for cage in dict_of_cages:
        dict_of_cages[cage]["Day"] = np.arange(len(dict_of_cages[cage]))

    return dict_of_cages

def plot_summary(dict_of_cages):
    for cage in dict_of_cages:
        sns.lineplot(data=dict_of_cages[cage], x='Day', y='Distance_meters')


def metrics(dict_of_cages):
    mouse_list = []
    for key in dict_of_cages.keys():
        mouse_list.append(key)
    max_meters = []
    avg_meters = []
    first_wk_meters = []
    last_wk_meters = []
    new_column_names = ['Mouse', 'Max_Meters_Day', 'Avg_Meters_Day', 'First_Wk_Meters_Day', 'Last_Wk_Meters_Day']

    for cage in dict_of_cages:
        max_meters.append(dict_of_cages[cage]["Distance_meters"].max())
        avg_meters.append(dict_of_cages[cage]["Distance_meters"].mean())
        first_wk_meters.append(dict_of_cages[cage]["Distance_meters"][0:7].mean())
        last_wk_meters.append(dict_of_cages[cage]["Distance_meters"][-7:].mean())

    wheel_summary_data = pd.DataFrame(list(zip(mouse_list, max_meters, avg_meters, first_wk_meters, last_wk_meters)), columns=new_column_names)
    
    wheel_summary_long = pd.melt(wheel_summary_data, id_vars='Mouse',  var_name="measurement", value_name='meters')

    return wheel_summary_data, wheel_summary_long





