#!/usr/bin/env python3

import logging
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import RPi.GPIO as GPIO

load_dotenv()

relay = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, GPIO.LOW)

logging.basicConfig(level=logging.INFO)

dbusername = os.getenv("dbusername")
dbpassword = os.getenv("dbpassword")
dbhost = os.getenv("dbhost")
dbport = os.getenv("dbport")
dbname = os.getenv("dbname")

dburl = f'postgresql://{dbusername}:{dbpassword}@{dbhost}:{dbport}/{dbname}'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=dburl
db = SQLAlchemy(app)

class GoogleUserModel(db.Model):
    
    __tablename__ = 'googleuser'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    rents = db.relationship('RentModel', backref='googleuser', lazy=True)

    def __init__(self, id, name, rents):
        self.id = id
        self.name = name
        self.rents = rents

class RentModel(db.Model):
    
    __tablename__ = 'rent'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(40))
    username = db.Column(db.String(40))
    google_user_id = db.Column(db.Integer, db.ForeignKey('googleuser.id'))
    letterbox_id = db.Column(db.Integer, db.ForeignKey('letterbox.id'))

    def __init__(self, id, status, username, google_user_id, letterbox_id):
        self.id = id
        self.status = status
        self.username = username
        self.google_user_id = google_user_id
        self.letterbox_id = letterbox_id

class LetterboxModel(db.Model):

    __tablename__ = 'letterbox'
    id = db.Column(db.Integer, primary_key=True)
    rents = db.relationship('RentModel', backref='letterbox', lazy=True)
    status = db.Column(db.String(40))

    def __init__(self, id, rents, status):
        self.id = id
        self.rents = rents
        self.status = status


@app.route("/lock")
def lock():

    username = request.args.get("name")
    rent_id = request.args.get("rent_id")

    rent = RentModel.query.get(rent_id)
    letterbox = LetterboxModel.query.get(rent.letterbox.id)

    if not rent:
        return "No rent found."

    if not letterbox:
        return "No mailbox found."


    if rent.username == username and letterbox.status == 'locked' and rent.status == 'ongoing':
        letterbox.status = 'unlocked'
        db.session.commit()
        logging.info('User ' + username + ' unlocked letterbox ' + str(letterbox.id) + ' linked to the rent ' + str(rent_id))
        GPIO.output(relay, GPIO.HIGH)
        return "Unlocked"

    elif rent.username == username and letterbox.status == 'unlocked' and rent.status == 'ongoing':
        letterbox.status = 'locked'
        db.session.commit()
        logging.info('User ' + username + ' locked letterbox ' + str(letterbox.id) + ' linked to the rent ' + str(rent_id))
        GPIO.output(relay, GPIO.LOW)
        return "Locked"

    else:
        return "Wrong owner for this letterbox or this rent is expired."




if __name__ == "__main__":
            app.run(host='0.0.0.0')
