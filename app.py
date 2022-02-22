import datetime
import pickle as pk

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '123456789'

# Conexion a la BBDD
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:artiel@35.195.232.151:3306/happy-adventure"
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.DateTime, nullable=False)
    edad = db.Column(db.Float, nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    amigos = db.Column(db.Float, nullable=False)
    punto_compra = db.Column(db.String(10), nullable=False)
    segmento = db.Column(db.String(10), nullable=False)
    producto_A = db.Column(db.Float, nullable=False)
    producto_B = db.Column(db.Float, nullable=False)
    probabilidad = db.Column(db.Float, nullable=False)

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


@app.route('/sentView', methods=['POST'])
def sentView():
    data = pd.DataFrame(request.form.to_dict(flat=False))

    # Convertimos a numericas las variables necesarias
    data = data.astype({'age': 'float', 'friends': 'float',
                'prodA': 'float', 'prodB': 'float'})

    data_original = data.copy()
    data = data.rename(columns={'age': 'Edad', 'gender': 'Sexo', 'friends': 'Acompaniantes_amigos',
        'prodA': 'Producto_A', 'prodB': 'Producto_B', 'punto-compra': 'Punto_Compra',
        'segmento': 'Segmento_cliente'})

    # Preparación de BBDD
    data['Producto_total'] = data['Producto_A'] + data['Producto_B']
    data['Producto_total_log'] = np.log(data['Producto_total'] + 1)

    data['Sexo_female'] = 0
    data.loc[data['Sexo'] == 'female','Sexo_female'] = 1

    data['Punto_Compra_S'] = 0
    data.loc[data['Punto_Compra'] == 'S','Punto_Compra_S'] = 1

    data['Segmento_cliente_1'] = 0
    data.loc[data['Segmento_cliente'] == '1','Segmento_cliente_1'] = 1
    data['Segmento_cliente_2'] = 0
    data.loc[data['Segmento_cliente'] == '2','Segmento_cliente_2'] = 1
    data['Segmento_cliente_3'] = 0
    data.loc[data['Segmento_cliente'] == '3','Segmento_cliente_3'] = 1

    quitar = ['Sexo', 'Producto_A', 'Producto_B', 'Producto_total', 
            'Punto_Compra', 'Segmento_cliente']
    data = data.drop(quitar, axis=1)

    prediction = modelo.predict(data)

    data_original['probabilidad'] = prediction
	
    hora = datetime.datetime.now()

    registro = Scores(
        hora = hora,
		edad = data_original['age'].values[0], 
        sexo = data_original['gender'].values[0],
        amigos = data_original['friends'].values[0], 
        punto_compra = data_original['punto-compra'].values[0],
        segmento = data_original['segmento'].values[0],
        producto_A = data_original['prodA'].values[0], 
        producto_B = data_original['prodB'].values[0],
        probabilidad = data_original['probabilidad'].values[0] 
    )

    db.session.add(registro)
    db.session.commit()

    return render_template('survey_completed.html', probabilidad = round(data_original['probabilidad'].values[0] * 100))	


if (__name__=="__main__"):
    # Código para leer el modelo entrenado
    modelo = pk.load(open('modelo_rl.sav', 'rb'))

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
