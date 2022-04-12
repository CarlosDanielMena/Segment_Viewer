#-*- coding: utf-8 -*- 
########################################################################
#SEGMENT_VIEWER.py

#Author   : Carlos Daniel Hernández Mena
#Date     : April 05th, 2022
#Location : Radboud University

#Usage:

#	$ python3 SEGMENT_VIEWER.py

#Example:

#	$ python3 SEGMENT_VIEWER.py

#Description:

#This is a python3 template.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import re
import os

########################################################################
#CONTROL PANEL

PATH_RUFA_TGS = "/mnt/Datos/VARIOS_PROGRAMAS/MFA/RESULTADOS_NETHERLANDS/TextGrids_RUFA"

PATH_MFA_TGS  = "/mnt/Datos/VARIOS_PROGRAMAS/MFA/RESULTADOS_NETHERLANDS/TextGrids_MFA"

PATH_WAVS     = "/mnt/Datos/VARIOS_PROGRAMAS/MFA/tutorial/Librispeech"

THRES_WORD_LEVEL=0.05 #50ms
THRES_PHONE_LEVEL=0.02 #20ms

########################################################################
########################################################################
########################################################################
#GLOBAL FUNCTIONS
########################################################################
########################################################################
########################################################################
def read_tg_items(tg_path_in,item_type):
	archivo_tg = open(tg_path_in,'r')
	if item_type=="WORD":
		patron_type=r'name = \"word'
	elif item_type=="PHONEME":
		patron_type=r'name = \"phone'
	elif item_type=="TRANSCRIPTION":
		patron_type=r'name = \"transcription'
	#ENDIF
	patron_item=r'item \[\d\]'
	CAPTURA=False
	BUSCA_INICIO=False
	XMIN=0.0
	XMAX=0.0
	TEXT=""
	LISTA_OUT=[]
	for linea in archivo_tg:
		#Quita el salto de linea de la linea actual
		linea = linea.replace("\n","")		
		linea = linea.strip()
		busca_patron_type=re.match(patron_type, linea)
		if busca_patron_type!=None:
			BUSCA_INICIO=True
		#ENDIF
		if BUSCA_INICIO==True:
			if linea == "intervals [1]:":
				CAPTURA=True
			#ENDIF
		#ENDIF		
		if CAPTURA==True:
			busca_patron_item=re.match(patron_item, linea)
			if busca_patron_item!=None:
				CAPTURA=False
				BUSCA_INICIO=False
			else:
				lista_linea=linea.split(" ")
				if lista_linea[0]=="xmin":
					XMIN=lista_linea[-1]
				elif lista_linea[0]=="xmax":
					XMAX=lista_linea[-1]
				elif lista_linea[0]=="text":
					lista_linea.pop(0)
					lista_linea.pop(0)
					TEXT=" ".join(lista_linea)
					TEXT=TEXT.replace("\"","")
					
					if item_type=="TRANSCRIPTION":
						TEXT=TEXT.lower()
					else:
						TEXT=TEXT.replace("\'","")
					#ENDIF
					if TEXT=="":
						#n. means "NONE"
						TEXT="n."
					#ENDIF
					LISTA_OUT.append([TEXT,XMIN,XMAX])
				#ENDIF
			#ENDIF
		#ENDIF	
	#ENDFOR
	archivo_tg.close()
	return LISTA_OUT
#ENDDEF
########################################################################
def find_files_in_paths(string_ending, searching_path):
	HASH_OUT={}
	for root, dirs, files in os.walk(searching_path):
		for filename in files:		
			if filename.endswith(string_ending):
				path_to_file=os.path.join(root,filename)
				clave=filename.replace(string_ending,"")
				HASH_OUT[clave]=path_to_file
			#ENDIF
		#ENDFOR
	#ENDFOR
	return HASH_OUT
#ENDDEF
########################################################################
def add_button(TIMESTEPS, COLOR, CAPTION, NAME):
	linea_out="<input class=\"addMore\" title=\""
	linea_out=linea_out+TIMESTEPS+"\" style=\"background-color:"
	linea_out=linea_out+COLOR+";\" type=\"submit\" value=\""
	linea_out=linea_out+CAPTION+"\" name=\""
	linea_out=linea_out+NAME+"\" />\n"
	return linea_out
#ENDDEF
########################################################################
def compare_timesteps(tupla_rufa,tupla_mfa):
	COLOR="green"
	ini_rufa=float(tupla_rufa[-2])
	ini_mfa=float(tupla_mfa[-2])
	fin_rufa=float(tupla_rufa[-1])
	fin_mfa=float(tupla_mfa[-1])
	dif_ini=round(abs(ini_rufa-ini_mfa),3)
	if dif_ini > THRES_WORD_LEVEL:
		COLOR="white"
	#ENDIF	
	dif_fin=round(abs(fin_rufa-fin_mfa),3)
	if dif_fin > THRES_WORD_LEVEL:
		COLOR="white"
	#ENDIF	
	return COLOR
#ENDDEF
########################################################################
def determine_colors(trans,lista_rufa_words,lista_mfa_words):
	lista_trans=trans.split(" ")
	#Determine valid tuples for RUFA
	lista_valid_rufa=[]
	for tupla in lista_rufa_words:
		word = tupla[0]
		if word in lista_trans:
			lista_valid_rufa.append(tupla)
		#ENDFOR
	#ENDFOR
	#Determine valid tuples for MFA
	lista_valid_mfa=[]
	for tupla in lista_mfa_words:
		word = tupla[0]
		if word in lista_trans:
			lista_valid_mfa.append(tupla)
		#ENDFOR
	#ENDFOR
	#Determine the colors
	lista_rufa_colors=[]
	lista_mfa_colors=[]
	for index in range(0,len(lista_valid_rufa)):
		COLOR=compare_timesteps(lista_valid_rufa[index],lista_valid_mfa[index])
		tupla_rufa=lista_valid_rufa[index]
		tupla_rufa.append(COLOR)
		lista_rufa_colors.append(tupla_rufa)
		tupla_mfa=lista_valid_mfa[index]
		tupla_mfa.append(COLOR)
		lista_mfa_colors.append(tupla_mfa)
	#ENDFOR
	return [lista_rufa_colors, lista_mfa_colors]
#ENDDEF
########################################################################
########################################################################
########################################################################
#MAIN PROGRAM
########################################################################
########################################################################
########################################################################
#FIND THE PATHS TO IMPORTANT FILES

HASH_RUFA_TG_PATHS=find_files_in_paths("_aligned.TextGrid",PATH_RUFA_TGS)

HASH_MFA_TG_PATHS=find_files_in_paths(".TextGrid",PATH_MFA_TGS)

HASH_WAV_PATHS=find_files_in_paths(".wav",PATH_WAVS)

########################################################################
#Sort the audio file keys

LISTA_KEYS = list(HASH_WAV_PATHS.items())
LISTA_KEYS.sort()

########################################################################
#GENERATE THE HTML PAGE
########################################################################
#Create the folder "templates"
if not os.path.exists("templates"):
	os.mkdir("templates")
#ENDIF

#Create the HTML file
archivo_out=open('templates/WORD_VIEW.html','w')

archivo_out.write("<!DOCTYPE html>\n")
archivo_out.write("<html>\n")

archivo_out.write("<head>\n")
archivo_out.write("<title> ")
archivo_out.write("SEGMENT VIEWER: Word View")
archivo_out.write(" </title>\n")
archivo_out.write("</head>\n")

archivo_out.write("<body>\n")

archivo_out.write("<H1>SEGMENT VIEWER: Word View</H1>\n")
archivo_out.write("<br>\n")
archivo_out.write("<br>\n\n")

#Put a hidden button

archivo_out.write("<form method=\"post\" action=\"/\">\n")
archivo_out.write("<input style=\"visibility:hidden;\" type=\"submit\" value=\"HIDDEN\" name=\"do_nothing\"/>\n")
archivo_out.write("</form>\n\n")

########################################################################
#Add the buttons

#This hash will help to create the python code
HASH_BUTTONS={}
CONT=0
for clave, nada in LISTA_KEYS:
	CONT=CONT+1
	#--------------------------------------------------------------#
	#Get the transcription and other information
	lista_trans=read_tg_items(HASH_RUFA_TG_PATHS[clave],'TRANSCRIPTION')
	audio_path=HASH_WAV_PATHS[clave]
	trans = lista_trans[0][0]
	duration = lista_trans[0][-1]
	#--------------------------------------------------------------#
	#Extract the timesteps of the current item
	lista_rufa_words=read_tg_items(HASH_RUFA_TG_PATHS[clave],'WORD')
	lista_mfa_words =read_tg_items(HASH_MFA_TG_PATHS[clave],'WORD')
	
	[lista_rufa_colors, lista_mfa_colors]=determine_colors(trans,lista_rufa_words,lista_mfa_words)
		
	#--------------------------------------------------------------#
	#Header for the Audio Item
	archivo_out.write("<form method=\"post\" action=\"/\">\n")
	
	linea_html="<H3>"+str(CONT)+") "+clave+"</H3>\n"
	archivo_out.write(linea_html)
	linea_html="<nobr><b>"+trans+"</b></nobr><br>\n"
	archivo_out.write(linea_html)
	linea_html="<nobr>Duration: "+duration+"</nobr><br>\n"
	archivo_out.write(linea_html)
	linea_html="<nobr>Path to Audio: "+audio_path+"</nobr><br><nobr>\n\n"####
	archivo_out.write(linea_html)

	#--------------------------------------------------------------#
	#Adding Button to identify RUFA transcription
	duration_parameter="0 - "+duration
	name_parameter=clave+"_rufa"
	linea_boton=add_button(duration_parameter,"red","RUFA",name_parameter)
	archivo_out.write(linea_boton)
	
	HASH_BUTTONS[name_parameter]=["RUFA", audio_path, "0",duration]
	#--------------------------------------------------------------#
	#Buttons for the RUFA transcription
	cont=-1
	#for tupla in lista_mfa_words:
	for tupla in lista_rufa_colors:
		cont=cont+1
		ini=tupla[-3]
		fin=tupla[-2]
		dur_par=ini+" - "+fin
		color_par=tupla[-1]
		cap_par=tupla[0]
		name_par=clave+"_rufa_"+str(cont)
		
		linea_boton=add_button(dur_par,color_par,cap_par,name_par)
		archivo_out.write(linea_boton)
		
		HASH_BUTTONS[name_par]=[cap_par, audio_path, ini, fin]
	#ENDFOR
	archivo_out.write("</nobr></form>\n\n") ####
	
	#--------------------------------------------------------------#
	#Adding Button to identify MFA transcription
	archivo_out.write("<form method=\"post\" action=\"/\"><nobr>\n")###
	
	duration_parameter="0 - "+duration
	name_parameter=clave+"_mfa"
	linea_boton=add_button(duration_parameter,"blue","MFA&nbsp;&nbsp;",name_parameter)
	archivo_out.write(linea_boton)
	
	HASH_BUTTONS[name_parameter]=["MFA", audio_path, "0",duration]
	#--------------------------------------------------------------#	
	#Buttons for the MFA transcription
	cont=-1
	#for tupla in lista_rufa_words:
	for tupla in lista_mfa_colors:
		cont=cont+1
		ini=tupla[-3]
		fin=tupla[-2]
		dur_par=ini+" - "+fin
		color_par=tupla[-1]
		cap_par=tupla[0]
		name_par=clave+"_mfa_"+str(cont)
		
		linea_boton=add_button(dur_par,color_par,cap_par,name_par)
		archivo_out.write(linea_boton)
		
		HASH_BUTTONS[name_par]=[cap_par, audio_path, ini, fin]
	#ENDFOR	

	archivo_out.write("</nobr></form>\n") ###
	#--------------------------------------------------------------#	
	archivo_out.write("\n<br>\n")
	archivo_out.write("<br>\n\n")
#ENDFOR

########################################################################
#Print HTML Footer
archivo_out.write("<footer><center>&copy; Copyright 2022. Radboud University in Colaboration with Reykjavik University. Carlos Mena. All Rights Reserved.</center></footer>\n")
archivo_out.write("</body>\n")
archivo_out.write("</html>\n")

archivo_out.close()

########################################################################
########################################################################
########################################################################
#GENERATE THE PYTHON CODE
########################################################################
########################################################################
########################################################################

########################################################################
#Main Functions for the Python Code
########################################################################
def add_button_elif(nombre_button,tupla_boton):
	valor=tupla_boton[0]
	path=tupla_boton[1]
	ini=tupla_boton[2]
	fin=tupla_boton[3]
	linea_elif="\t\telif request.form.get(\'"+nombre_button+"\') == \'"+valor+"\':\n"
	system_command="play "+path+" trim "+ini+" ="+fin
	linea_action="\t\t\tos.system(\'"+system_command+"\')\n"
	linea_out=linea_elif+linea_action
	return linea_out
#ENDDEF

########################################################################
#SAVE THE HASH OF BUTTONS AND ACTIONS IN A FILE
archivo_db=open("button_actions.db",'w')

for b_name in HASH_BUTTONS:
	tupla_b=HASH_BUTTONS[b_name]
	audio_path=tupla_b[1]
	fin=tupla_b[-1]
	ini=tupla_b[-2]
	linea_out=b_name+" "+audio_path+" "+ini+" "+fin
	archivo_db.write(linea_out+"\n")
#ENDFOR
archivo_db.close()

########################################################################
#Create the file
archivo_out=open("RUN_SV.py",'w')

archivo_out.write("#-*- coding: utf-8 -*-\n\n")

archivo_out.write("#Open the link:\n")
archivo_out.write("#http://127.0.0.1:5000/\n\n")

archivo_out.write("from flask import Flask, render_template, request\n")
archivo_out.write("app = Flask(__name__)\n\n")
archivo_out.write("import os\n\n")

archivo_out.write("#Load the database of buttons and actions.\n")
archivo_out.write("HASH_BOTONES={}\n")
archivo_out.write("archivo_db=open(\'button_actions.db\',\'r\')\n")
archivo_out.write("for linea in archivo_db:\n")
archivo_out.write("\tlinea=linea.replace(\"\\n\",\"\")\n")
archivo_out.write("\tlista_linea=linea.split(\" \")\n")
archivo_out.write("\tboton_id=lista_linea[0]\n")
archivo_out.write("\tlista_linea.pop(0)\n")
archivo_out.write("\tHASH_BOTONES[boton_id]=lista_linea\n")
archivo_out.write("#ENDFOR\n")
archivo_out.write("archivo_db.close()\n\n")

archivo_out.write("@app.route(\"/\", methods=[\'GET\', \'POST\'])\n\n")
archivo_out.write("def index():\n")

archivo_out.write("\tif request.method == \'POST\':\n")

#----------------------------------------------------------------------#
#Add button actions
#----------------------------------------------------------------------#
archivo_out.write("\t\tdata_from_form=str(request.form)\n")
archivo_out.write("\t\tdata_from_form=data_from_form.replace(\"ImmutableMultiDict([(\\\'\",\"\")\n")
archivo_out.write("\t\tdata_from_form=data_from_form.replace(\"\\\')])\",\"\")\n")
archivo_out.write("\t\tdata_from_form=data_from_form.replace(\"\\\', \\\'\",\" \")\n")
archivo_out.write("\t\tlista_data=data_from_form.split(\" \")\n")
archivo_out.write("\t\tboton_actual=lista_data[0]\n")
archivo_out.write("\t\ttupla_action=HASH_BOTONES[boton_actual]\n")
archivo_out.write("\t\tpath=tupla_action[0]\n")
archivo_out.write("\t\tini=tupla_action[1]\n")
archivo_out.write("\t\tfin=tupla_action[2]\n")
archivo_out.write("\t\tcomando=\'play \'+path+\' trim \'+ini+\' =\'+fin\n")
archivo_out.write("\t\tos.system(comando)\n")
#----------------------------------------------------------------------#
#archivo_out.write("\t\t#ENDIF\n")
archivo_out.write("\t#ENDIF\n")
archivo_out.write("\treturn render_template(\"WORD_VIEW.html\")\n")
archivo_out.write("#ENDDEF\n\n")

archivo_out.write("app.run(host=\'0.0.0.0\', port=5000)\n")

#Close the file
archivo_out.close()
########################################################################
print("Run the SEGMENT VIEWER TYPING:")
print("python3 RUN_SV.py\n")
print("And open this link in your browser:")
print("http://127.0.0.1:5000/")
########################################################################

