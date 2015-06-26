#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

"""
ical.py
"""

import os
from icalendar import Calendar, Event
from datetime import datetime, timedelta
#from icalendar.parser import q_split, q_join
import requests
import requests_cache
#import traceback
#import logging
#import logging.config
import pandas as pd
#import numpy as np
import time
import datetime
import ical_lire_carte

from config import config

def vevents_to_dataframe(cal):
    """
    Conversion des datetime
    """
    lst_components = []
    for i, component in enumerate(cal.walk(name="VEVENT")):
        lst_components.append(component)
    df = pd.DataFrame(lst_components)
    for col in ['DTSTART', 'DTEND', 'LAST-MODIFIED', 'DTSTAMP', 'CREATED']:
        df[col] = pd.to_datetime(df[col].map(lambda x: x.dt))
    return(df)

basepath = '.'

filename = os.path.join(basepath, "requests_cache")
requests_cache.install_cache(filename, backend='sqlite', expire_after=300) #expiration seconds

jour = time.strftime('%Y-%m-%d', time.localtime())
params = {
    'firstDate':jour,
    'lastDate':jour,
    'projectId':5
}

url = "https://upplanning6.appli.univ-poitiers.fr/jsp/custom/modules/plannings/direct_cal.jsp?login={login}&password={password}&code=C14R018&calType=ical".format(login=config['login'], password=config['password'])

r = requests.get(url, params=params)
dat = r.text

cal = Calendar.from_ical(dat)

df_cal = vevents_to_dataframe(cal)
df_cal2 = df_cal[['DTSTART', 'DTEND', 'DESCRIPTION', 'SUMMARY', 'LOCATION']]

desc = df_cal['DESCRIPTION']

for elt in desc.index:
    vt = desc.get_value(elt)
    vtl = vt.to_ical()

s = desc.get_value(0)

ds = df_cal.DESCRIPTION[0:10].to_string

ll = s.to_ical()

col = ['JOUR', 'DEBUT', 'FIN', 'GROUPE', 'ENSEIGNANT', 'ETUDIANTS', 'EFFECTIF']

df_cal2['JOUR'] = ''
df_cal2['DEBUT'] = ''
df_cal2['FIN'] = ''
df_cal2['GROUPE'] = ''
df_cal2['ENSEIGNANT'] = ''
df_cal2['ETUDIANTS'] = ''
df_cal2['EFFECTIF'] = ''
#df_cal2[0:2]

#Colonne Groupe et Enseignant
for i, elt in enumerate(desc):
    toto = elt.to_ical().split('\\n')
    df_cal2.GROUPE[i] = toto[1]
    df_cal2.ENSEIGNANT[i] = toto[2]

#Heure Debut cours et jour
for i, x in enumerate(df_cal['DTSTART']):
    hd = x.strftime('%Y-%m-%d %H:%M:%S')
    utc = datetime.datetime.now()-datetime.datetime.utcnow()
    date_select = datetime.datetime.strptime(hd, '%Y-%m-%d %H:%M:%S' )
    delta = timedelta(seconds=utc.seconds+1)
    date_debut = date_select + delta
    df_cal2.DEBUT[i] = date_debut.strftime('%H:%M:%S')
    df_cal2.JOUR[i] = date_debut.strftime('%Y-%m-%d')
    
#Heure Fin cours
for i, x in enumerate(df_cal['DTEND']):
    hf = x.strftime('%Y-%m-%d %H:%M:%S')
    utc = datetime.datetime.now()-datetime.datetime.utcnow()
    date_select = datetime.datetime.strptime(hf, '%Y-%m-%d %H:%M:%S' )
    delta = timedelta(seconds =utc.seconds+1)
    date_fin = date_select + delta
    df_cal2.FIN[i] = date_fin.strftime('%H:%M:%S')

df_cal2.pop('DESCRIPTION')
df_cal2.pop('DTSTART')
df_cal2.pop('DTEND')
print df_cal2[0:10]

rep = '0'    #Lis obligatoirement une carte
liste_etu = []
liste_rep = ['o', 'O', '0']
d = -1
f = 1

while rep in liste_rep:

    dict_etu = ical_lire_carte.lecture()
    heure = dict_etu['h']
    grp = dict_etu['grp']
    etu = dict_etu['etu']

    #Compare heure passage
    for a in enumerate(df_cal2['DEBUT']):
        for b in enumerate(df_cal2['FIN']):
            if a[1] <= heure <= b[1] and a[0] == b[0]:
                d = a[0]
    f = f+d

    #Compare Groupe et demi-groupe
    ajout = 0
    vide = []
    if grp[:7] == df_cal2.GROUPE[d][:7] and (df_cal2.GROUPE[d][7:] == vide or grp[7:] == df_cal2.GROUPE[d][7:]):
        if liste_etu == []:
            ajout = 1
        for x in liste_etu:
            if x == etu:
                ajout = 0
                break
            else:
                ajout = 1

    if ajout == 1:
        liste_etu.append(etu)

    #Ajout etudiants présents et effectif
    df_cal2.ETUDIANTS[d] = '\n'.join(liste_etu)
    df_cal2.EFFECTIF[d] = len(liste_etu)
    print '\n', df_cal2[d:f]

    heure_rap = time.strftime('%H:%M:%S', time.localtime())
    if heure_rap >= df_cal2.FIN[d]:
        break

    rep = raw_input("\nLire une autre carte ?(O:oui/N:non)")

while heure_rap < df_cal2.FIN[d]:    #Boucle si arret lecture
    time.sleep(1)
    heure_rap = time.strftime('%H:%M:%S', time.localtime())

df_cal2[d:f].to_excel('rapport.xls', sheet_name='Sheet1')
print "\nRapport généré en excel"
