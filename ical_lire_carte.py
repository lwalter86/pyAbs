#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
ical_lire_carte.py
"""

import sqlite3
import nxppy
import time
#import datetime

def lecture():
    """
    lecture de carte etudiante
    """
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
            print "\tUID:", uid

            etudiant['h'] = time.strftime('%H:%M:%S', time.localtime())    #Heure de passage de la carte

            cursor.execute('SELECT uid FROM Etudiants')
            liste = cursor.fetchall()

            valeur = 1

            for i in liste:
                if uid != i[0]:        #UID inconnu dans la bdd
                    valeur = 1
                else:                #UID connu dans la bdd
                    valeur = 0
                    #Affiche le groupe
                    cursor.execute('SELECT groupe FROM Etudiants WHERE uid=?', (uid,))
                    groupe_etu = cursor.fetchone()
                    for groupe in groupe_etu:
                        etudiant['grp'] = groupe

                    #Affiche le nom et le prénom
                    cursor.execute('SELECT nom FROM Etudiants WHERE uid=?', (uid,))
                    nom_etu = cursor.fetchone()
                    for nom in nom_etu:
                        nom_etu = nom

                    cursor.execute('SELECT prenom FROM Etudiants WHERE uid=?', (uid,))
                    prenom_etu = cursor.fetchone()
                    for prenom in prenom_etu:
                        etudiant['etu'] = nom_etu + ' ' + prenom
                    break

            if valeur == 1:
                print "\n\tErreur: Aucun UID correspondant"
            return etudiant
        except nxppy.SelectError:
            pass

    connection.commit()
    cursor.close()