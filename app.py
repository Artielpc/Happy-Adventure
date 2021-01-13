from flask import Flask, request, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import os
import pandas as pd
import random
import datetime


app = Flask(__name__)
app.secret_key = '123456789'

# Conexion a la BBDD
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:almena@35.234.68.236:3306/mascarillas"
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    ip = db.Column(db.String(20), nullable=True)
    date = db.Column(db.DateTime, nullable=False)

db.create_all()


# diccionarios para gestionar las fotos y valoraciones
pictures = os.listdir("static/img/Persons")
SCORE = ['score_01', 'score_02', 'score_03', 'score_04' ,'score_05',
    'score_06', 'score_07' ,'score_08' ,'score_09' ,'score_10']


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500




@app.route('/', methods=['GET'])
def index():
    # Creamos las imagenes aleatorias que se van a mostrar
	aux = random.sample(range(1,int(len(pictures)/2+1)),10)

	for i in range(0,len(aux)):
		aux[i] = str(aux[i]).zfill(2)
		if (i % 2 == 1):
			aux[i] = 'static/img/Persons/person_' + aux[i] + '_mask.jpg'
		else:
			aux[i] = 'static/img/Persons/person_' + aux[i] + '.jpg'

	session["imagenes_usadas"] = aux
        
	return render_template('index.html', pics = aux, score = SCORE)	


@app.route('/sentView', methods=['POST','GET'])
def sentView():
	if request.method == 'POST':
		ip = request.remote_addr
		ip = ip.replace('.','')
		ip = ip[3:]

		# Añadimos las 10 votaciones a la base de datos
		s = {}
		registro = {}
		time = datetime.datetime.now()
		for i in range(0,10):
			try:
				s[i] = request.form[SCORE[i]]
			except:
				s[i] = 99
			registro[i] = Scores(person=session["imagenes_usadas"][i], score=s[i], 
			age=request.form['age'], gender=request.form['gender'], ip=ip,
            date = time)

			db.session.add(registro[i])

		db.session.commit()

	return render_template('survey_completed.html')	


if (__name__=="__main__"):
	app.run(debug=False, threaded=True)
