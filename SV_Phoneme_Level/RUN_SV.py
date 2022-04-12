#-*- coding: utf-8 -*-

#Open the link:
#http://127.0.0.1:5000/

from flask import Flask, render_template, request
app = Flask(__name__)

import os

#Load the database of buttons and actions.
HASH_BOTONES={}
archivo_db=open('button_actions.db','r')
for linea in archivo_db:
	linea=linea.replace("\n","")
	lista_linea=linea.split(" ")
	boton_id=lista_linea[0]
	lista_linea.pop(0)
	HASH_BOTONES[boton_id]=lista_linea
#ENDFOR
archivo_db.close()

@app.route("/", methods=['GET', 'POST'])

def index():
	if request.method == 'POST':
		data_from_form=str(request.form)
		data_from_form=data_from_form.replace("ImmutableMultiDict([(\'","")
		data_from_form=data_from_form.replace("\')])","")
		data_from_form=data_from_form.replace("\', \'"," ")
		lista_data=data_from_form.split(" ")
		boton_actual=lista_data[0]
		tupla_action=HASH_BOTONES[boton_actual]
		path=tupla_action[0]
		ini=tupla_action[1]
		fin=tupla_action[2]
		comando='play '+path+' trim '+ini+' ='+fin
		os.system(comando)
	#ENDIF
	return render_template("PHONEME_VIEW.html")
#ENDDEF

app.run(host='0.0.0.0', port=5000)
