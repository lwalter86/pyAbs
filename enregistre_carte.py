#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
enregistre_carte.py

PB : la carte doit être présente quand on choisi de lire une nouvelle carte
sinon plantage
2015-06-29
"""
from __future__ import print_function
import nxppy
import sqlite3
import time
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")

file_handler = RotatingFileHandler('debug.log', mode="a", maxBytes= 100000000, backupCount= 1)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
    
steam_handler = logging.StreamHandler()
steam_handler.setFormatter(formatter)
steam_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(steam_handler)


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

    print("\nPassez la carte")
    carte = nxppy.Mifare()

    try:
        carte_etu['uid'] = carte.select()		#Lecture UID de la carte
        logger.debug("Carte détectée")
        logger.debug("UID:", carte_etu['uid'])
        #logger.debug(carte_etu['heure'], "\n", carte_etu['jour'])

        #Données à écrire
        carte_etu['nom'] = raw_input("Entrer le nom : ")
        carte_etu['prenom'] = raw_input("Entrer le prenom : ")
        carte_etu['groupe'] = raw_input("Entrer le semestre et le groupe : (ex: GE-S1-A1)")

        return carte_etu
            
    except nxppy.SelectError:	#Si pas de carte, retour "try"	
        pass																		

def create_table(dbname):
    try:
        db = sqlite3.connect(dbname)
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Etudiants(
                              id INTEGER PRIMARY KEY,
                              uid VARCHAR,
                              jour DATE,
                              heure TIME,
                              nom VARCHAR,
                              prenom VARCHAR,
                              groupe VARCHAR)''')

        db.commit()
        logger.info("Table créée")
        
    except Exception as e:
        # Roll back any change if something goes wrong
        logger.info("Erreur lors de la creation de la table")
        db.rollback()
        raise e
    
    finally:
        db.close()
      
def enregistre(bdd):
    """
    Enregistrement d'une carte nfc dans la BDD
    """
    carte_etu = lecture_carte()
    
    logger.debug(carte_etu)
    
    uid = carte_etu['uid']
    jour = carte_etu['jour']
    heure = carte_etu['heure']
    nom = carte_etu['nom']
    prenom = carte_etu['prenom']
    groupe = carte_etu['groupe']

    try:
        db = sqlite3.connect(bdd)
        cursor = db.cursor()
        cursor.execute('SELECT uid FROM Etudiants')
        liste = cursor.fetchall()
        liste_uid = [x[0] for x in liste]
        if uid in liste_uid:
            logger.debug("UID déjà existant")
            cursor.execute("""UPDATE Etudiants SET groupe = ? WHERE uid = ?""", (groupe, uid, ))
            
        else:
            cursor.execute('''INSERT INTO Etudiants(uid, jour, heure, nom, prenom, groupe)
                                VALUES(?, ?, ?, ?, ?, ?)''', (uid, jour, heure, nom, prenom, groupe))    
            logger.info("Carte ajoutée")

    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    
    finally:
        db.close()
        
    #for uid in liste_uid:

        #if uid2 != uid:
    
        
def print_table(bdd):
    try:
        db = sqlite3.connect(bdd)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Etudiants')

        for i in cursor:
            print("*****\n")
            print("ID: ", i[0])
            print("UID: ", i[1])
            print("Jour: ", i[2])
            print("Heure: ", i[3])
            print("Nom: ", i[4])
            print("Prenom: ", i[5])
            print("Groupe: ", i[6])
        
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    
    finally:
        db.close()
        
def main():
    
    logger.info("START Script")
    
    dbname = "carte.db"
    
    #Connexion a la bdd
    #connection = sqlite3.connect(dbname)
    #logger.debug("Ouverture de la base de données")

    #cursor = connection.cursor()

    #Creation de la table
    create_table(dbname)

    #Boucle pour lire ou non carte
    rep = raw_input("Enregistrer une carte ?(O:oui/N:non)")
    liste = ['o', 'O', '0']
    while rep in liste:
        enregistre(dbname)
        rep = raw_input("\nEnregistrer une carte ? (O:oui/N:non)")
    else:
        logger.info("END Script")

    #connection.commit()

    #Ecriture des données
    print_table(dbname)

    #cursor.close()

if __name__ == "__main__":
    main()
