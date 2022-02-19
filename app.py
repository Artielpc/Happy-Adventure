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
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:artiel@35.195.147.6:3306/happy-adventure"
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.DateTime, nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    sexo = db.Column(db.String(6), nullable=False)
    amigos = db.Column(db.Integer, nullable=False)
    punto_compra = db.Column(db.String(1), nullable=True)
    segmento = db.Column(db.String(1), nullable=False)
    producto_A = db.Column(db.Float, nullable=False)
    producto_B = db.Column(db.Float, nullable=False)

db.create_all()



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')	


@app.route('/sentView', methods=['POST','GET'])
def sentView():
	print("Entro a sentView")
	if request.method == 'POST':
		print(request)



        
		
		hora = datetime.datetime.now()
		registro = Scores(
            hora = hora,
			edad = request.form['age'], 
            sexo = request.form['gender'],
            amigos = request.form['friends'], 
            punto_compra = request.form['punto-compra'],
            segmento = request.form['segmento'],
            producto_A = request.form['prodA'], 
            producto_B = request.form['prodB'],  
        )

		db.session.add(registro)
		db.session.commit()

	return render_template('survey_completed.html')	


if (__name__=="__main__"):
	app.run(debug=False, threaded=True)
