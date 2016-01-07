#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
enregistre_carte.py

PB : la carte doit être présente quand on choisi de lire une nouvelle carte
sinon plantage
2015-06-29
"""

import nxppy
import sqlite3
import time
#import lire_carte

def lecture_carte():		
    """
    Lecture de carte etudiante
    """
    carte_etu = {
        'uid' : '',
        'jour' : time.strftime('%Y-%m-%d', time.localtime()),
        'heure' : time.strftime('%H:%M:%S', time.localtime()),
        'nom' : '',
        'prenom' : '',
        'groupe' : ''
    }

    print "\nPasser la carte"
    carte = nxppy.Mifare()

    try:
        carte_etu['uid'] = carte.select()		#Lecture UID de la carte
        print "\nCarte détectée"
        print "UID:", carte_etu['uid']
        print carte_etu['heure'], "\n", carte_etu['jour']

        #Données à écrire
        carte_etu['nom'] = raw_input("Entrer le nom : ")
        carte_etu['prenom'] = raw_input("Entrer le prenom : ")
        carte_etu['groupe'] = raw_input("Entrer le semestre et le groupe : (ex: GE-S1-A1)")

        return carte_etu
            
    except nxppy.SelectError:	#Si pas de carte, retour "try"	
        pass																		


def enregistre():
    """
    Enregistrement d'une carte nfc dans la BDD
    """
    carte_etu = lecture_carte()
    
    print carte_etu
    
    uid = carte_etu['uid']
    jour = carte_etu['jour']
    heure = carte_etu['heure']
    nom = carte_etu['nom']
    prenom = carte_etu['prenom']
    groupe = carte_etu['groupe']

    cursor.execute('SELECT uid FROM Etudiants')
    liste_uid = cursor.fetchall()

    #Test si les valeurs sont connues
    ajout = 0
    for uid in liste_uid:

        if uid != uid[0]:    
            ajout = 1        #Valeurs a ajoutées        
        else:
            ajout = 0
            print "UID déjà existant"    
            cursor.execute("""UPDATE Etudiants SET groupe = ? WHERE uid = ?""", (groupe, uid, ))
            break

    if ajout != 0:     
        cursor.execute('''INSERT INTO Etudiants(uid, jour, heure, nom, prenom, groupe)
        VALUES(?, ?, ?, ?, ?, ?)''', (uid, jour, heure, nom, prenom, groupe))    
        print "Les valeurs ont été ajoutées"

        
def main():
    
    #Connexion a la bdd
    connection = sqlite3.connect('carte.db')
    print "\nOuverture de la base de données"

    cursor = connection.cursor()

    #Creation de la table
    cursor.execute("CREATE TABLE IF NOT EXISTS Etudiants(id INTEGER PRIMARY KEY, uid VARCHAR, jour DATE, heure TIME, nom VARCHAR, prenom VARCHAR, groupe VARCHAR)")
    print "Table créée"

    #Boucle pour lire ou non carte
    rep = raw_input("Enregistrer une carte ?(O:oui/N:non)")
    liste = ['o', 'O', '0']
    while rep in liste:
        enregistre()
        rep = raw_input("\nEnregistrer une carte ? (O:oui/N:non)")

    connection.commit()

    #Ecriture des données
    cursor.execute('SELECT * FROM Etudiants')

    for i in cursor:
        print "*****\n"
        print "ID: ", i[0]
        print "UID: ", i[1]
        print "Jour: ", i[2]
        print "Heure: ", i[3]
        print "Nom: ", i[4]
        print "Prenom: ", i[5]
        print "Groupe: ", i[6]

    cursor.close()

if __name__ == "__main__":
    main()
