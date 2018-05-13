from __future__ import division
from flask import Flask, abort, request, jsonify
import numpy as np
import pandas as pd
from scipy import signal
import json
import pymysql
from flask_cors import CORS

app = Flask(__name__)


@app.route('/porcentaje',methods=['GET','POST'])
def porcentaje():
    if request.method == 'POST':
        datos = request.json
        convert = pd.DataFrame.from_dict(datos, orient='index')
        coordenadas = convert.transpose()
        coordenadas = coordenadas.convert_objects(convert_numeric=True)
        picos = (coordenadas[['picos_x','picos_y']]).dropna(how='all')
        picos = picos.rename(columns={"picos_x": "x", "picos_y": "y"})
        coordenadas_x_y = coordenadas[['x','y']]
        xs = coordenadas_x_y.y
        datos = np.sin(xs)
        peakind = signal.find_peaks_cwt(datos, np.arange(0.1,1,0.1))
        resultado = pd.concat([coordenadas_x_y.x[peakind],coordenadas_x_y.y[peakind]], axis=1)
        porcentaje = pd.merge( picos, resultado, on=['x','y'] )
        result = {'porcentaje':((len(porcentaje.index)/len(picos.index))*100) }
        #result = {'resultado_size':len(picos.index)}
        return  jsonify(resultado)
        #return  resultado.to_json()
    if request.method == 'GET':
        return "Metodo GET"
    else:
        return "nada de nada"

@app.route("/gruposfuncionales",methods=['GET','POST'])
def gruposfuncionales():
    if request.method == 'POST':
        datos = request.json
        convert = pd.DataFrame.from_dict(datos, orient='index')
        coordenadas = convert.transpose()
        coordenadas = coordenadas.convert_objects(convert_numeric=True)
        picos = (coordenadas[['picos_x','picos_y']]).dropna(how='all')
        picos = picos.rename(columns={"picos_x": "x", "picos_y": "y"})

        conn = pymysql.connect(
            db='prueba',
            user='root',
            passwd='12345678',
            host='localhost')
        c = conn.cursor()

        c.execute("SELECT * FROM GruposFuncionales")

        rv = c.fetchall()
        payload = []
        content = {}
        for result in rv:
            content = {'id_GF': result[0],'id_Compuesto':result[1] ,'name_Compuesto': result[2],'name_GF': result[3] , 'Rango1': result[4],'Rango2':result[5]}
            payload.append(content)
            content = {}

        gruposDb = pd.DataFrame(payload)

        gruposFuncionales = []
        for index, row in gruposDb.iterrows():
            for index, coordenada in picos.iterrows():
                if coordenada.x in range(row['Rango1'],row['Rango2']):
                    gruposFuncionales.append({'x':coordenada.x,'y':coordenada.y,'id_GF': row['id_GF'], 'grupoF':row['name_GF'] , 'Rango1': row['Rango1'],'Rango2':row['Rango2']})
           
   
        return jsonify(gruposFuncionales)    

    if request.method == 'GET':
        return "Metodo Get"




@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://198.199.91.102')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


if __name__ == "__main__":
    app.run()
