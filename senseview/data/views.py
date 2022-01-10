from django.shortcuts import render
from tinydb import TinyDB, Query
from django.template import loader
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

def get_datetime_read_string(datetime_object):
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S")

def verifyPeriodPassed(currItemDateTime, lastItemDateTime):
    period = 10 * 60
    if currItemDateTime is None or lastItemDateTime is None:
        return True
    
    diffSeconds = (currItemDateTime - lastItemDateTime).total_seconds()
    
    if diffSeconds >= period:
        return True
    
    return False

def index(request, countHours=None):
    db = TinyDB('/home/pi/app/database/database/db.sensedata', create_dirs=True)
    # result = "<ul>"
    environment_data = db.all()
    labels = []
    dataTemp = []
    dataPress = []
    dataHum = []
    
    countHours = countHours * 4
    curr_datetime_object = None
    last_datetime_object = None
    for item in db:
        if item['pressure'] < 100:
            continue
        
        curr_datetime_object = datetime.strptime(item['date_time'],"%Y-%m-%d %H:%M:%S.%f%z")
        currItemDateTime = get_datetime_read_string(curr_datetime_object)
       
        if verifyPeriodPassed(curr_datetime_object, last_datetime_object):
            last_datetime_object = curr_datetime_object
            labels.append(currItemDateTime)
            # labels.append(curr_datetime_object.timestamp())
            dataTemp.append(item['temperature'])
            dataPress.append(item['pressure'])
            dataHum.append(item['humidity'])

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
    }

    # for item in db:
    #     result = result + f"<li>{item['date_time']} Temp: {item['temperature']} Hum: {item['humidity']} Press: {item['pressure']}</li>" 

    # result = result + "</ul>"
    return render(request, 'data/index.html', context)
