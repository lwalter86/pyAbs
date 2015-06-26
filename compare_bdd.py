#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
compare_bdd.py
"""

import sqlite3
import nxppy

def lire():
    """
    Lecture de la carte étudiant et vérification de la présence dans la base
    """
    print "\nPasser la carte"
    carte = nxppy.Mifare()
    uid = carte.select()
    print "\nCarte détectée"
    print "UID:", uid

    cursor.execute('SELECT uid FROM Etudiants')
    liste_uid_dans_bdd = cursor.fetchall()

    valeur = 0

    for i in liste_uid_dans_bdd:
        if uid != i[0]:
            #UID inconnu dans la bdd
            valeur = 1
        else:
            #UID connu dans la bdd
            valeur = 0
            print "UID Correspondant trouvé"
            break

    if valeur == 0:
        #Affiche les données
        cursor.execute('SELECT nom,prenom,groupe FROM Etudiants WHERE uid=?',(uid,))
        donnees_etu = cursor.fetchone()
        print "\n*****"
        for elt in donnees_etu:
            print elt
    else:
        print "\nErreur: Aucun UID correspondant"

def main():
    #Connexion a la bdd
    con_base = sqlite3.connect('carte.db')
    cursor = con_base.cursor()

    #Execution de la fonction
    rep = raw_input("*****\nRetrouver la carte dans la base ?(O:oui/N:non)")
    choix = ['o', 'O', '0']
    while rep in choix:
        lire()
        rep = raw_input("*****\nRetrouver la carte dans la base ?(O:oui/N:non)")

    con_base.commit()
    cursor.close()

if __name__ == '__main__':
    main()