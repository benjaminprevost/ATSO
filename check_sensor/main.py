#! /usr/bin/env python3
#-*- coding: utf-8 -*-

from datetime import datetime, timedelta, tzinfo
import requests
import os
import filecmp
from shutil import copyfile
import smtplib

account = {"email": os.environ.get("OPENSENSEMAP_EMAIL"),
           "password": os.environ.get("OPENSENSEMAP_PASSWORD"),
           "smtp_user": os.environ.get("SMTP_USER"),
           "smtp_password": os.environ.get("SMTP_PASSWORD"),
           "smtp_server": os.environ.get("SMTP_SERVER"),
           "to": os.environ.get("TO"),
           }

delay = 600
tmpDir = "tmp/"
tmpFile = "temp"
latestFile = "latest"

apiUrl = 'https://api.opensensemap.org/'
cred = {"email": account["email"], "password": account["password"]}

l = requests.post(apiUrl+'users/sign-in', json=cred)
auth_token = l.json()['token']
head = {'Authorization': 'Bearer ' + auth_token}
r = requests.get(apiUrl+'users/me/boxes', headers=head)

sensors = r.json()['data']['boxes']

def check_sensor(sensor):
    now = datetime.utcnow()
    name = sensor['name']
    result = {}
    result[name] = []

    for item in sensor['sensors']:
        try:
            last_check = datetime.fromisoformat(item['lastMeasurement']['createdAt'][:-1])
            deltaTmp = now - last_check
            delta = deltaTmp - timedelta(microseconds=deltaTmp.microseconds)

            if delta.total_seconds() > delay:
                result[name].append({"type": item['sensorType'], "title": item['title'], "delta": delta})
        except:
            delta = "No data"
            result[name].append({"type": item['sensorType'], "title": item['title'], "delta": delta})

    return result

def send_mail(content):

    subject = '[ATSO] capteur(s) en difficulté'
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (account["smtp_user"], account["to"], subject))

    for sensor in badCheck:
        msg = msg + sensor + '\n'
        for item in badCheck[sensor]:
            msg = msg + "\t" + item['type'] + " " + str(item['delta']) + "\n"

    with smtplib.SMTP(account["smtp_server"], 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(account["smtp_user"], account["smtp_password"])
        server.sendmail(account["smtp_user"], account["to"], msg.encode('utf8'))

if __name__ == '__main__':

    badCheck = {}
    for sensor in sensors:
        error = check_sensor(sensor)
        for key in error.keys():
            if len(error[key]) > 0:
                badCheck[key] = error[key]
                #print(*error, sep="\n")

    with open(tmpDir+tmpFile, 'w') as f:
        for sensor in badCheck:
            print(f"{sensor}")
            f.write("%s\n" % sensor)
            for item in badCheck[sensor]:
                print(f"{item['type']} ({item['delta']})")
                f.write("%s\n" % item['type'])

    if filecmp.cmp(tmpDir+tmpFile, tmpDir+latestFile):
        print('Status not changed')
    else:
        copyfile(tmpDir+tmpFile, tmpDir+latestFile)
        send_mail(badCheck)
