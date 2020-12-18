#! /usr/bin/env python3
from datetime import datetime, timedelta, tzinfo
import requests

api = "https://api.opensensemap.org/boxes/"
sensors = ['5fa2d69e67d8a1001be8687e', '5fac45e61fb9e3001bdddc95', '5fc29f623a7437001bf6022c', '5fc290c73a7437001bef6c20']

def check_sensor(id):
    r = requests.get(api+id)
    
    now = datetime.utcnow()
    data = r.json()
    name = data['name']

    for item in data['sensors']:
        try:
            last_check = datetime.fromisoformat(item['lastMeasurement']['createdAt'][:-1])
            delta = now-last_check
            if delta.total_seconds() > 600:
                print(name, item['sensorType'], item['title'], delta)
        except:
            delta = 'No data'
            print(name, item['sensorType'], item['title'], delta)

    return None


if __name__ == '__main__':

    for sensor in sensors:
        check_sensor(sensor)
