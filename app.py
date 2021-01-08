from flask import Flask, request, render_template, redirect, url_for, session, flash, Markup, send_from_directory
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
import base64
import numpy as np
import os
import pandas as pd
import random
from werkzeug.utils import secure_filename
import json
import time
import socket
from datetime import datetime


app = Flask(__name__)
app.secret_key = '123456789'

# Conexion a la BBDD
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:almena@35.234.68.236:3306/mascarillas"
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Resultados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(40), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Numeric, nullable=False)
    user_id = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

db.create_all()




# diccionario para gestionar las valoraciones
session_dict = {}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
	print("ESTA ES UNA PRUEBA")

	return render_template('index.html')	


@app.route('/scoreImagesView', methods=['POST','GET'])
def scoreImagesView():
	print("OK")
	if request.method == 'POST':
		print(request.form)

		aux = Resultados(fname=request.form['fname'], lname=request.form['lname'], 
        email=request.form['email'], gender=request.form['gender'], birthdate=request.form['birthdate'])

		db.session.add(aux)
		db.session.commit()

	return render_template('score_images.html')	


@app.route('/sentView', methods=['POST','GET'])
def sentView():
	print("OK")
	if request.method == 'POST':
		print(request.form)

	return render_template('survey_completed.html')	


if (__name__=="__main__"):
	app.run(debug=False, threaded=True)
