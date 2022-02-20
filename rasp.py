#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:@localhost:5432/rasp'

db = SQLAlchemy(app)

class Location(db.Model):
	__tablename__='locations'
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(40))
	porte=db.Column(db.String(40))

	def __init__(self, id, username, porte):
		self.id = id
		self.username = username
		self.porte = porte



@app.route("/lock")
def lock():

	location = Location.query.get(1)
	if not location:
		return "Aucune location trouvée"


	if location.username == 'axel' and location.porte == 'closed':
		location.porte = 'open'
		db.session.commit()		
		return "Ouverture"

	elif location.username == 'axel' and location.porte == 'open':
		location.porte = 'closed'
		db.session.commit()
		return "Fermeture"

	else:
		return "Ce n'est pas votre location"





if __name__ == "__main__":
            app.run()
