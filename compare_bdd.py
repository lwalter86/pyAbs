#!/usr/bin/python
#-*- coding: utf-8 -*-

import sqlite3
import nxppy

def lire():
	print "\nPasser la carte"
	carte=nxppy.Mifare()
	uid = carte.select()
	print "\nCarte détectée"
	print "UID:",uid

	cursor.execute('SELECT uid FROM Etudiants')
	liste = cursor.fetchall()

	valeur = 0

	for i in liste:
		if uid != i[0]:
			valeur = 1			#UID inconnu dans la bdd
		else:
			valeur = 0			#UID connu dans la bdd
			print "UID Correspondant trouvé"
			break

	if valeur == 0:
		#Affiche les données
		cursor.execute('SELECT nom,prenom,groupe FROM Etudiants WHERE uid=?',(uid,))
		tuple = cursor.fetchone()
		print "\n*****"
		for x in tuple:
			print x
	else:
		print "\nErreur: Aucun UID correspondant"

#Connexion a la bdd
connection = sqlite3.connect('carte.db')
cursor = connection.cursor()

#Execution de la fonction
rep = raw_input("*****\nRetrouver la carte dans la base ?(O:oui/N:non)")
liste = ['o','O','0']
while rep in liste:
	lire()
	rep = raw_input("*****\nRetrouver la carte dans la base ?(O:oui/N:non)")

connection.commit()
cursor.close()	