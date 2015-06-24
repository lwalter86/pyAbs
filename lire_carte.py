#!/usr/bin/python
#-*- coding: utf-8 -*-

# Lecture d'une carte NFC

import nxppy	
import time	

def lecture_carte():		

	dict = {
	    'uid' : '',
		'jour' : time.strftime('%Y-%m-%d',time.localtime()),
		'heure' : time.strftime('%H:%M:%S',time.localtime()),
		'nom' : '',
		'prenom' : '',
		'groupe' : ''
		}

	print "\nPasser la carte"
	carte=nxppy.Mifare()

        try:
			dict['uid'] = carte.select()		#Lecture UID de la carte
			print "\nCarte détectée"
			print "UID:",dict['uid']
			print dict['heure'],"\n",dict['jour']

			#Données à écrire
			dict['nom'] = raw_input("Entrer le nom : ")
			dict['prenom'] = raw_input("Entrer le prenom : ")
			dict['groupe'] = raw_input("Entrer le semestre et le groupe : (ex: GE-S1-A1)")

			return dict
        except nxppy.SelectError:	#Si pas de carte, retour "try"	
			pass																		
