import os
import time
import cv2
from flask import Flask, request, render_template
from multiping import MultiPing
from datetime import date, datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib

app = Flask(__name__)

kailai = ["172.16.89.23", "KAILAINATHAN"]
ironman = ["172.16.90.71", "kishan"]
mentor = ["172.16.87.90", "SHERIN"]
kishan = ["172.16.89.207", "gausic"]

list1 = [mentor, kishan]
list2 = [kailai, ironman]

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
nimgs = 10

def studentsearch(ip):
    mp = MultiPing([ip])
    mp.send()
    responses, _ = mp.receive(1)
    return bool(responses)

def extract_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
    return face_points

@app.route('/')
def check_students():
    for depname in [list1, list2]:
        for emp in depname:
            time.sleep(2) 
            EmpStatus = studentsearch(emp[0])
            if EmpStatus:
                print("Student {} Is Here - Time Stamp {}".format(emp[1], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                os.system('python main.py')
            else:
                print("Student {} Is Not Here - Time Stamp {}".format(emp[1], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return "No students found."


if __name__ == "__main__":
    app.run(debug=True)
    


