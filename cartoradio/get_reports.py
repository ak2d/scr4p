from fileinput import filename
import requests
import multiprocessing as mp
from pathlib import Path
from PyPDF2 import PdfFileReader
import os
import ssl
import http.client
import re
import multiprocessing as mp
from tqdm import tqdm
import csv
import argparse
global writer
global anciennete

from datetime import datetime


import tempfile

# /home/akd/.local/lib/python3.9/site-packages/urllib3/connectionpool.py:1045: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.cartoradio.fr'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_measures(dept):
    url = "https://www.cartoradio.fr/api/v1/mesures?=&stationsRadioelec=true&objetsCom=false&anciennete=" + str(anciennete) + "&valeurLimiteMin=0&valeurLimiteMax=87&format=geojson&departement=" + str(dept)
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    data = response.json
    res = []
    try : 
        for i in data()['features']:
            res.append(i['id'])
            #ids.put(i['id'])
            #print(i['id'])
    except KeyError as e:
        print("no data for dept " + str(dept))
    return(res)


def check_is_mesure_exist(o):
    for i in o:
        if isinstance(i, list):
            is_exist = check_is_mesure_exist(i)
        else:
            if i.title == "Résultat de la mesure spécifique*":
                
                return i
        if 'is_exist' in locals() and is_exist != None:
            return is_exist
                

def regex_val(txt):
    rawvalues = re.findall(r'[0-9]*\.?[0-9]* V\/m', txt)

    values=[]
    for i in rawvalues:
        values.append(float(i[:-3]))

    return values
   
def get_mesure(fichier):
    signets = fichier.outline

    is_mesure_exist=check_is_mesure_exist(signets)
    if is_mesure_exist != None:
        npage=fichier.get_destination_page_number(is_mesure_exist)
        page=fichier.getPage(npage)

        txt=page.extractText()
        splited=str.splitlines(txt)
        #print(splited)
        result={}
        if "rateurChamp" in txt:
            splited=str.splitlines(txt)
            #print(splited)
            for i in splited:
                if "ORANGE" in i:
                    result["ORANGE"]=regex_val(i)
                if "FREE" in i:
                    result["FREE"]=regex_val(i)
                if "SFR" in i:
                    result["SFR"]=regex_val(i)
                if "BOUYGUES" in i:
                    result["BOUYGUES"]=regex_val(i)
        else:
            if "ORANGE" in txt:
                result["ORANGE"]=regex_val(txt)
            if "FREE" in txt:
                result["FREE"]=regex_val(txt)
            if "SFR" in txt:
                result["SFR"]=regex_val(txt)
            if "BOUYGUES" in txt:
                result["BOUYGUES"]=regex_val(txt)

        return(result)

def download_and_process_file(report):
    # Create a temporary file
    with tempfile.TemporaryFile() as temp:
        url = "https://www.cartoradio.fr/cartoradio/web/rapports/" + str(report)
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)    

        temp.write(response.content)

        return(get_mesure(PdfFileReader(temp)))


def get_report_value(measure):
    url = "https://www.cartoradio.fr/api/v1/mesures/" + str(measure)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    data = response.json
    try : 
        if data()['data']['laboratoire'] == "EXEM":
            val = download_and_process_file(data()['data']['rapport'])
            if isinstance(val, dict):
                #print(str(measure) + " / " +  str(data()['data']['rapport']) + "  ↪  " + str(val))
                res = []
                #for operator, v in val.items():
                #    res = (str(measure), operator, v)
                #return([str(measure), k, v])
                return([str(measure), val])
            else:
                #print(str(measure) + " / " +  str(data()['data']['rapport']) + "  ↪  No data")
                pass
    except KeyError as e:
        pass

def run_for_dept(dept):
    #print(get_measures(dept))
    #for mes in get_measures(dept):
    with mp.Pool(50) as p:
        return(p.map(get_report_value, get_measures(dept)))
    
# Structure : mesures par dept ==> get report par mesure ==> download + récupération de la mesure ==> return ==> write to csv

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--anciennete', type=int, default=720, help='Recherche sur X derniers jours')
    args = parser.parse_args()
    anciennete = args.anciennete

    current_datetime = datetime.now()
    str_current_datetime = str(current_datetime)
    file_name = str_current_datetime + "_" + str(anciennete) + ".csv"

    with open(file_name,'w') as f:
        writer = csv.writer(f, delimiter=";")
        # ici nous parcourons tous parcourons tous les départements
        for dept in tqdm(range(1, 100)):
            res = run_for_dept(dept)
            for r in res:
                try:
                    for k, v in r[1].items():
                        row = [str(r[0]),  str(k)]
                        for w in v:
                            row.append(str(w))
                        writer.writerow(row)                        
                        tqdm.write(str(row))
                except (csv.Error, TypeError, AttributeError) as e:
                    pass
        f.close()

