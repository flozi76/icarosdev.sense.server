from django.shortcuts import render
from tinydb import TinyDB, Query
from django.template import loader
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

def get_datetime_read_string(datetime_object):
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S")

def verifyPeriodPassed(currItemDateTime, lastItemDateTime):
    period = 5 * 60 # take one per five minutes
    if currItemDateTime is None or lastItemDateTime is None:
        return True
    
    diffSeconds = (currItemDateTime - lastItemDateTime).total_seconds()
    
    if diffSeconds >= period:
        return True
    
    return False

def add_item_to_dictionary(item_dictionary, json_object):
    device_name = json_object['raspi_name']
    
    if not item_dictionary.get(device_name):
        item_dictionary[device_name] = []
    
    item_dictionary[device_name].append(json_object)

def index(request, countHours=None):
    db = TinyDB('/home/pi/app/database/database/db.sensedata', create_dirs=True)
    
    item_dictionary = dict()
    data_keys_dictionary = dict() # add datakeys per device type to generate diagrams automatically.
    
    environment_data = db.all()
    labels = []
    dataTemp = []
    dataPress = []
    dataHum = []
    
    countHours = countHours * 6
    
    curr_datetime_object = None
    last_datetime_object = None
    for item in db:
        data = item['env_data']
        
        if data['pressure'] < 100:
            continue
        
        curr_datetime_object = datetime.strptime(item['date_time'],"%Y-%m-%d %H:%M:%S.%f%z")
       
        # if verifyPeriodPassed(curr_datetime_object, last_datetime_object):
        add_item_to_dictionary(item_dictionary, item)
        
        # last_datetime_object = curr_datetime_object
        currItemDateTime = get_datetime_read_string(curr_datetime_object)
        labels.append(currItemDateTime)
        dataTemp.append(data['temperature'])
        dataPress.append(data['pressure'])
        dataHum.append(data['humidity'])



    labels = labels[-countHours:]
    dataTemp = dataTemp[-countHours:]
    dataPress = dataPress[-countHours:]
    dataHum = dataHum[-countHours:]

    context = {
        'environment_data': environment_data,
        'labels': labels,
        'dataTemp': dataTemp,
        'dataPress': dataPress,
        'dataHum': dataHum,
        'item_dictionary' : item_dictionary,
    }

    # for item in db:
    #     result = result + f"<li>{item['date_time']} Temp: {item['temperature']} Hum: {item['humidity']} Press: {item['pressure']}</li>" 

    # result = result + "</ul>"
    return render(request, 'data/index.html', context)
