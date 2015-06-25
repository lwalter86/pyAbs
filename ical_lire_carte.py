#!/usr/bin/python
#-*- coding: utf-8 -*-

import sqlite3
import nxppy
import time
import datetime

def lecture():
	#Connexion a la bdd
    connection = sqlite3.connect('carte.db')
    cursor = connection.cursor()

    etudiant = {
        'h' : '',
        'grp' : '',
        'etu' : ''
        }

    print "\nPasser la carte"
    carte = nxppy.Mifare()

    while True:
        try:
            uid = carte.select()    #Lecture de la carte
            print "\n\tCarte détectée"
            print "\tUID:",uid

            etudiant['h'] = time.strftime('%H:%M:%S',time.localtime())    #Heure de passage de la carte

            cursor.execute('SELECT uid FROM Etudiants')
            liste = cursor.fetchall()

            valeur = 1

            for i in liste:
                if uid != i[0]:        #UID inconnu dans la bdd
                    valeur = 1
                else:                #UID connu dans la bdd
                    valeur = 0
                    #Affiche le groupe
                    cursor.execute('SELECT groupe FROM Etudiants WHERE uid=?',(uid,))
                    tuple = cursor.fetchone()
                    for x in tuple:
                        etudiant['grp'] = x

                    #Affiche le nom et le prénom
                    cursor.execute('SELECT nom FROM Etudiants WHERE uid=?',(uid,))
                    tuple = cursor.fetchone()
                    for x in tuple:
                        nom = x

                    cursor.execute('SELECT prenom FROM Etudiants WHERE uid=?',(uid,))
                    tuple = cursor.fetchone()
                    for x in tuple:
                        etudiant['etu'] = nom + ' ' + x
                    break

            if valeur == 1:
                print "\n\tErreur: Aucun UID correspondant"
            return etudiant
        except nxppy.SelectError:
            pass

    connection.commit()
    cursor.close()