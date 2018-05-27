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
        resultado = resultado[resultado.y > 0.01]
        porcentaje = pd.merge( picos, resultado, on=['x'] )
        json_result = {'porcentaje':((len(porcentaje.index)/len(picos.index))*100),'picos_x':resultado.x.values.tolist(),'picos_y':resultado.y.values.tolist()}
        #result = {'porcentaje':((len(porcentaje.index)/len(picos.index))*100),'picos':resultado}
        #result = {'resultado_size':len(picos.index)}
        return  jsonify(json_result)
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
            content = {'id_GF': result[0],'id_Compuesto':result[1] ,'name_Compuesto': result[2],'name_GF': result[3] , 'Rango1': result[4],'Rango2':result[5],'estado':result[6]}
            payload.append(content)
            content = {}

        gruposDb = pd.DataFrame(payload)

        gruposFuncionales = []
        for index, row in gruposDb.iterrows():
            for index, coordenada in picos.iterrows():
                if int(coordenada.x) in range(row['Rango1'],row['Rango2']):  
                    gruposFuncionales.append({'x':coordenada.x,'y':coordenada.y,'id_GF': row['id_GF'], 'grupoF':row['name_GF'] , 'Rango1': row['Rango1'],'Rango2':row['Rango2'],'estado':row['estado']})
        
        GF = pd.DataFrame(gruposFuncionales)
        compuestoEstado = []
        uniqueGF = GF.drop_duplicates(subset='grupoF', keep="last")
        for estado in uniqueGF.estado:
            compuestoEstado.append(estado)

        dfa = {0:{'0':1, '1':3},
               1:{'0':17, '1':2},
               2:{'0':17, '1':12},
               3:{'0':16, '1':4},
               4:{'0':6, '1':5},
               5:{'0':17, '1':7},
               6:{'0':9, '1':8},
               7:{'0':'Yeso-Crudo', '1':'Yeso-Crudo'},
               8:{'0':'Basanita', '1':'Basanita'},
               9:{'0':17, '1':11},
               10:{'0':16, '1':15},
               11:{'0':'Anhidrita', '1':'Anhidrita'},
               12:{'0':'Cuarzo', '1':'Cuarzo'},
               16:{'0':17, '1':18},
               18:{'0':'Calcita-Cuarzo', '1':'Calcita-Cuarzo'},
               17:{'0':'No se encontró', '1':'No se encontró'}
              }


        def accepts(transitions,initial,accepting,s):
            state = initial
            for c in s :
                if state in accepting:
                    state = transitions[state][str(gruFun[str(state)])]
                    return state 
                else:
                    state = transitions[state][str(gruFun[str(state)])]
            return state 
            
        gruFun={}
        for key in dfa:
            if key in compuestoEstado:
                 state = 1 
            else: 
                state = 0
            gruFun[str(key)]=state 

        compuesto = accepts(dfa,0,{7,12,8,11,18,17},gruFun)
        
        compuestosGF = {'GruposFuncionales':gruposFuncionales,'Compuesto':compuesto}                 
        return jsonify(compuestosGF)    

    if request.method == 'GET':
        return "Metodo Get"


@app.route('/Compuesto',methods=['GET','POST'])
def compuesto():
    if request.method == 'POST':
        datos = request.json
        tableGF = pd.DataFrame(datos)
        uniqueGF = tableGF.drop_duplicates(subset='grupoF', keep="last")
        sumaPonderacion = 0
        for ponderacion in uniqueGF.Ponderacion:
            sumaPonderacion = ponderacion + sumaPonderacion

        if sumaPonderacion == 30:
            compuesto = 'Yeso-Crudo'
        if sumaPonderacion == 20:
            compuesto = 'Basanita'
        if sumaPonderacion == 19:
            compuesto = 'Anhidrita'
        if sumaPonderacion == 24:
            compuesto = 'Calcita-Cuarzo'
        if sumaPonderacion == 31:
            compuesto = 'Calcita-Cuarzo'   

        Compuesto = {'Compuesto':compuesto}
        return jsonify(Compuesto)    
   

    if request.method == 'GET':
        return "Metodo GET"


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://198.199.91.102')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


if __name__ == "__main__":
    app.run()
