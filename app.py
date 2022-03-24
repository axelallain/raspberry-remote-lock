#!/usr/bin/env python3

import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:@localhost:5432/rasp'
db = SQLAlchemy(app)

class LetterboxModel(db.Model):

        __tablename__ = 'letterbox'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(40))
        status = db.Column(db.String(40))

        def __init__(self, id, username, status):
                self.id = id
                self.username = username
                self.status = status


@app.route("/lock")
def lock():
	username = request.args.get("name")

	letterbox = LetterboxModel.query.get(1)
	if not letterbox:
		return "No mailbox found."


	if letterbox.username == username and letterbox.status == 'locked':
		letterbox.status = 'unlocked'
		db.session.commit()		
		logging.info('User ' + username + ' unlocked letterbox ' + str(letterbox.id))
		return "Unlocked"

	elif letterbox.username == username and letterbox.status == 'unlocked':
		letterbox.status = 'locked'
		db.session.commit()
		logging.info('User ' + username + ' locked letterbox ' + str(letterbox.id))
		return "Locked"

	else:
		return "Wrong owner for this letterbox."





if __name__ == "__main__":
            app.run()
