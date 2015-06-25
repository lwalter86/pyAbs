#!/usr/bin/python
#-*- coding: utf-8 -*-

# Lecture d'une carte NFC

import nxppy	
import time	

def lecture_carte():		

	carte_etu = {
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
			carte_etu['uid'] = carte.select()		#Lecture UID de la carte
			print "\nCarte détectée"
			print "UID:",carte_etu['uid']
			print carte_etu['heure'],"\n",carte_etu['jour']

			#Données à écrire
			carte_etu['nom'] = raw_input("Entrer le nom : ")
			carte_etu['prenom'] = raw_input("Entrer le prenom : ")
			carte_etu['groupe'] = raw_input("Entrer le semestre et le groupe : (ex: GE-S1-A1)")

			return carte_etu
            
        except nxppy.SelectError:	#Si pas de carte, retour "try"	
			pass																		
