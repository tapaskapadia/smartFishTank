import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime
import time
import pymysql
import sys

HOSTNAME = "sensordata.cxvfjw9upbqk.us-east-1.rds.amazonaws.com"
USERNAME = 'root'
PASSWORD = 'password'
DB_NAME = 'sensorstuff'
connection = pymysql.connect(host=HOSTNAME,
                                 user=USERNAME,
                                 passwd=PASSWORD,
                                 db=DB_NAME,
                                 port=3306,
                                 autocommit=True,
                                 cursorclass=pymysql.cursors.DictCursor)
connection.autocommit(True)

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def start_skill():
	msg = "Welcome to the fish tank app. Please say your command" 
	return question(msg).reprompt("Do you have another command?")
	# welcome_msg = "Would you like to know the external or internal temperature?"
	# return question(welcome_msg)

@ask.intent("InternalIntent")
def internal_temperature():
	with connection.cursor() as cursor:
		sql = "SELECT * FROM Temp ORDER BY ID desc LIMIT 1"
		cursor.execute(sql)
		result = cursor.fetchone()
	curTime = result['TS']
	month = curTime.strftime("%I %M")
	msg = "The current internal temperature is %.2f degrees fahrenheit recorded at %s . Is there something else you would like me to do?" % (result['V'],month)
	return question(msg).reprompt("Do you have another command?")

@ask.intent("LightsOnIntent")
def lights_on():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','1')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Turning on the lights. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("LightsOffIntent")
def lights_off():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','0')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Turning off the lights. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("RaiseBrightnessIntent")
def raise_brightness():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','+')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Raising the brightness. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("LowerBrightnessIntent")
def lower_brightness():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','-')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Lowering the brightness. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("PatternIntent")
def pattern():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','p')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Changing the pattern. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("AmbientModeIntent")
def ambient_mode():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','a')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Switching to ambient mode. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("ManualModeIntent")
def manual_mode():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','m')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Switching to manual mode. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("FeedIntent")
def feed():
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	with connection.cursor() as cursor:
		sql = "INSERT INTO Alexa (TS,Code) VALUE ('%s','=')" % (timestamp)
		cursor.execute(sql)
	msg = "Okay. Feeding the fish. Is there something else you would like me to do?"
	return question(msg).reprompt("Do you have another command?")

@ask.intent("NoIntent")
def no():
	return statement("Okay. Bye then.")

if __name__ == '__main__':
    app.run(debug=True)