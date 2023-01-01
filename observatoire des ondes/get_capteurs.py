import requests
import string
import random
import json
import datetime
import csv
import base64
import os
import pandas as pd

HERE = os.path.dirname(__file__)

file_name = input("Jeu de données initial (tapez juste entrée pour ignorer) : ")
file_name = file_name.rstrip()
file_path = os.path.join(HERE, file_name)

if file_name.rstrip() == '':
    print("Pas de fichier en entrée, extraction de tous les capteurs")
    file_path = False
elif os.path.isfile(file_path):
    print("Fichier {file_path} en entrée".format(file_path=file_path))
else:
    raise RuntimeError("Le fichier {file_path} n'existe pas".format(file_path=file_path))

output_path = os.path.join(HERE, "output_2.xlsx")

y = input("Année à extraire (tapez juste entrée pour extraire toutes les valeurs) : ")
y = y.rstrip()

if y == '':
    year = False
    print("Extraction de toutes les valeurs")
else:
    try:
        year = int(y)
        if year < 2020:
            raise RuntimeError("L'année minimum est 2020")
        print ("Extration des valeurs pour l'année {year}".format(year=str(year)))
    except:
        raise RuntimeError("L'année entrée n'est pas valide")

excluded = []
df_infos = pd.DataFrame({'ville': [], 'code_postal': [], 'numero': []})
if file_path != False:
    df = pd.read_excel (file_path, 'Sheet1')

    df.pop("id")
    df.pop("E^2")
    df.pop("Année")
    df.pop("Mois")
    df.pop("Jour")

    for index,row in df.iterrows():
        if row["numero"] not in excluded:
            excluded.append(row["numero"])
            df_prov = pd.DataFrame({'ville': [row["ville"]], 'code_postal': [row["code_postal"]], 'numero': [row["numero"]]})
            df_infos=pd.concat([df_infos,df_prov])

    df.pop("ville")
    df.pop("code_postal")
else:
    df = pd.DataFrame({'E_volt_par_metre': [], 'date': [], 'numero': []})

#print(df_infos)
#print(df)

def gen_zx():
    zx = ""
    for i in range(12):
        zx = zx+random.choice(string.ascii_lowercase+string.digits)
    return zx

RID = str(random.randint(0, 999999999))
zx = gen_zx()

headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", "Alt-Used": "firestore.googleapis.com","Connection": "keep-alive", "Content-Length": "460", "Content-Type": "application/x-www-form-urlencoded", "Host": "firestore.googleapis.com", "Origin": "https://www.observatoiredesondes.com", "Referer" :"https://www.observatoiredesondes.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0"}
url = "https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?database=projects/odo-prod/databases/(default)&VER=8&RID="+RID+"&CVER=22&X-HTTP-Session-Id=gsessionid&$httpHeaders=X-Goog-Api-Client:gl-js/ fire/8.2.2 Content-Type:text/plain &zx="+zx+"&t=1"

body = "count=1&ofs=0&req0___data__=%7B%22database%22%3A%22projects%2Fodo-prod%2Fdatabases%2F(default)%22%2C%22addTarget%22%3A%7B%22query%22%3A%7B%22structuredQuery%22%3A%7B%22from%22%3A%5B%7B%22collectionId%22%3A%22public_sites%22%7D%5D%2C%22orderBy%22%3A%5B%7B%22field%22%3A%7B%22fieldPath%22%3A%22__name__%22%7D%2C%22direction%22%3A%22ASCENDING%22%7D%5D%7D%2C%22parent%22%3A%22projects%2Fodo-prod%2Fdatabases%2F(default)%2Fdocuments%22%7D%2C%22targetId%22%3A2%7D%7D"

r = requests.post(url, headers = headers, data = body)

SID = r.text.split("\"")[3]
gsessionid = r.headers["X-HTTP-Session-Id"]

zx = gen_zx()
#zx = "enh2pjgund83"
#zx = "snzink2d0wy5"
#zx = "o1fz1swlykqm"
#zx = "9xyfb5rfzgia"
#zx = "6d0gll4dzkgl"
#zx = "zbu56em5waq5"

headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", "Connection": "keep-alive", "DNT": "1", "Host": "firestore.googleapis.com", "Origin": "https://www.observatoiredesondes.com", "Referer" :"https://www.observatoiredesondes.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0"}
url = "https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?database=projects/odo-prod/databases/(default)&gsessionid="+gsessionid+"&VER=8&RID=rpc&SID="+SID+"&CI=0&AID=0&TYPE=xmlhttp&zx="+zx+"&t=1"

before = datetime.datetime.now()
r = requests.get(url, headers = headers)
after = datetime.datetime.now()

temps = after-before

print("Temps de la requête = "+str(temps))
print("Header:")
print(r.headers)
print("Body:")
#print(r.text[:1000])

output = r.text

output = output[output.find("\n")+1:]

size = int(output[output.rfind("[[")+2:output.rfind(",[")])

last = ""

for i in range(1,size+1):
    if last == "":
        last = output.find("["+str(i))
    else:
        debut = output[last:].find("{")+last
        fin = output[:output.find("["+str(i))].rfind("}")+1
        if output[last:].find("{") != -1 and output[last:output.find("["+str(i))].rfind("}") != -1:
            #print ("\n\n\n\n\n\n"+output[debut:fin])
            data = json.loads(output[debut:fin])
            if data.get("documentChange") != None:
                #print (data["documentChange"])
                if data["documentChange"].get("document") != None:
                    if data["documentChange"]["document"].get("fields") != None:
                        if data["documentChange"]["document"]["fields"].get("exem_id") != None:
                            name = data["documentChange"]["document"]["fields"]["exem_id"]["stringValue"]
                            if name not in excluded:
                                id = data["documentChange"]["document"]["fields"]["id"]["stringValue"]
                                current_value = data["documentChange"]["document"]["fields"]["current_value"]["doubleValue"]
                                min_value = data["documentChange"]["document"]["fields"]["min_8_days"]["doubleValue"]
                                average_value = data["documentChange"]["document"]["fields"]["avg_8_days"]["doubleValue"]
                                max_value = data["documentChange"]["document"]["fields"]["max_8_days"]["doubleValue"]
                                zip_code = str(data["documentChange"]["document"]["fields"]["zip_code"]["stringValue"])
                                city = data["documentChange"]["document"]["fields"]["city"]["stringValue"]
                                address = data["documentChange"]["document"]["fields"]["address"]["stringValue"]
                                country = data["documentChange"]["document"]["fields"]["country"]["stringValue"]
                                status = data["documentChange"]["document"]["fields"]["status"]["stringValue"]
                                latitude = data["documentChange"]["document"]["fields"]["geolocation"]["mapValue"]["fields"]["latitude"]["doubleValue"]
                                longitude = data["documentChange"]["document"]["fields"]["geolocation"]["mapValue"]["fields"]["longitude"]["doubleValue"]
                                installation_date = data["documentChange"]["document"]["fields"]["installation_date"]["timestampValue"]
                                #print ("#####"+name+"#####\nID : "+id+"\nCurrent : "+str(current_value)+"\nMin : "+str(min_value)+"\nAverage : "+str(average_value)+"\nMax : "+str(max_value)+"\n")
                                df_prov = pd.DataFrame({'ville': [city], 'code_postal': [zip_code], 'numero': [name]})
                                df_infos = pd.concat([df_infos,df_prov])


                                headers_values = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3","Connection": "keep-alive", "Host": "odo-prod.ey.r.appspot.com", "Origin": "https://www.observatoiredesondes.com", "Referer": "https://www.observatoiredesondes.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0"}
                                url_values = "https://odo-prod.ey.r.appspot.com/public_datas/"+id
                                r_values = requests.get(url_values, headers = headers_values)
                                print(id)
                                output_values = base64.b64decode(r_values.text).decode()
                                data = json.loads(output_values)

                                for values in data["values"]:
                                    timestamp = datetime.datetime.fromtimestamp(values["date"])
                                    if not year or timestamp.year == year:
                                        value = values["value"]
                                        df_prov = pd.DataFrame({"E_volt_par_metre": [value],"date": [timestamp],"numero": [name]})
                                        df=pd.concat([df,df_prov])

        last = output.find("["+str(i))

print(df_infos)
print(df)
with pd.ExcelWriter(output_path) as writer:
    df_infos.to_excel(writer, sheet_name='Capteurs', index=False)
    df.to_excel(writer, sheet_name='Valeurs', index=False)