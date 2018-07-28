#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response,jsonify
import time
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera
import serial
import RPi.GPIO as GPIO
import database
import random
import datetime
import glob
import boto3
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera
app = Flask(__name__)

ACCESS_KEY=""
SECRET_KEY=""
REGION="us-east-1"
#get sns

client = boto3.client('sns', aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name=REGION)
connection = database.get_connection()
Sent = False
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template(generate())
def generate():
    yield 'index.html'

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/lightOn")
def light():
    response = 'Light On Succesful'
    print "DOG DOG"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('1')
    except:
      response = 'Failure'
    return response

@app.route("/lightOff")
def lightO():
    response = "Light Off Succesful"
    print "CAT CAT"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('0')
    except:
      response = 'Failure'
    return response

@app.route("/ambient")
def ambient():
    response = 'index.html'
    print "A A"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('a')
    except:
      response = 'Failure'
    return response
@app.route("/ambientOff")
def ambientOff():
    response = 'index.html'
    print "A A"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('m')
    except:
      response = 'Failure'
    return response
@app.route("/dim")
def dim():
    response = 'index.html'
    print "D A"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('-')
    except:
      response = 'Failure'
    return response

@app.route("/brighten")
def bright():
    response = 'Succesful'
    print "B A"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('+')
    except:
      response = 'Failure'
    return response

@app.route("/feed")
def feed():
    response = 'index.html'
    print "B A"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('=')
    except:
      response = 'index.html'
    return "Succesful"

@app.route("/pattern")
def pattern():
    response = 'index.html'
    print "P A"
    try:
      usbCom = serial.Serial('/dev/ttyACM0',9600)
      usbCom.write('p')
    except:
      response = 'index.html'
    return "Succesful"

@app.route("/postTemp",methods=['POST'])
def postT():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
    x = temp_f
    global Sent
    if ((x > 84 or x < 70) and not Sent):
        response = client.publish(
                TargetArn="arn:aws:sns:us-east-1:426036099940:ece4813-final",
                Message="Watch Out: " + str(x),
                MessageStructure='string',
                Subject='Fish Alert'
        )
        Sent = True
    elif (not(x > 84 or x < 70)):
        Sent = False
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print timestamp
    with connection.cursor() as cursor:
        statement = "INSERT INTO Temp (TS,V) VALUES ('"+timestamp+ "','"+str(x)+"');"
        cursor.execute(statement)
        statement = "SELECT * From Alexa WHERE TS > '"+datetime.datetime.fromtimestamp(ts-5).strftime('%Y-%m-%d %H:%M:%S')+"' ORDER BY TS DESC LIMIT 1"
        cursor.execute(statement)
        results = cursor.fetchall()
        if(len(results)):
            print results[0]['Code']
            try:
                usbCom = serial.Serial('/dev/ttyACM0',9600)
                usbCom.write(results[0]['Code'])
            except:
                print "nothing"
    return str(x)

@app.route("/data")
def gT():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    timestampOld = datetime.datetime.fromtimestamp(ts-60).strftime('%Y-%m-%d %H:%M:%S')

    with connection.cursor() as cursor:
        statement = "SELECT TS as timestamp, V as temperature FROM Temp WHERE TS > '"+timestampOld+ "' ORDER BY TS DESC LIMIT 1"
        cursor.execute(statement)
        results = cursor.fetchall()
        print results
        return jsonify(results[0])

@app.route('/watchStream')
def watch():
    return render_template('watchStream.html')
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', threaded=False)
    finally:
        connection.close()

