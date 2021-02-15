from flask import Flask, render_template, jsonify
import requests
import os

account = {"email": os.environ.get("OPENSENSEMAP_EMAIL"),
           "password": os.environ.get("OPENSENSEMAP_PASSWORD"),
           }

app = Flask(__name__)

@app.route('/opensensormapavg/')
def sensoravg():

    apiOpenSenseMap = 'https://api.opensensemap.org/'
    cred = {'email': account['email'], 'password': account['password']}

    l = requests.post(apiOpenSenseMap + 'users/sign-in' , json=cred)
    auth_token = l.json()['token']
    head = {'Authorization': 'Bearer ' + auth_token}
    r = requests.get(apiOpenSenseMap + 'users/me/boxes', headers=head)

    sensors = r.json()['data']['boxes']
    
    Measure = {"h": [], "l": []}

    for sensor in sensors:
        if sensor['exposure'] == "outdoor":
            for item in sensor['sensors']:
                if item['sensorType'] == "SDS 011" and 'lastMeasurement' in item.keys():
                    if item['title'] == "PM10":
                        try:
                            Measure['h'].append(float(item['lastMeasurement']['value']))
                        except:
                            pass
                    elif item['title'] == "PM2.5":
                        try:
                            Measure['l'].append(float(item['lastMeasurement']['value']))
                        except:
                            pass

    avg = {'avgL': sum(Measure['l'])/len(Measure['l']), 'avgH': sum(Measure['h'])/len(Measure['h'])}

    return render_template("average.html", avg=avg)

if __name__ == "__main__":
    app.run(debug=True)