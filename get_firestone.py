import requests
import string
import random
import json
import datetime

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
                            site = data["documentChange"]["document"]["fields"]["exem_id"]["stringValue"]
                            id = data["documentChange"]["document"]["fields"]["id"]["stringValue"]
                            current_value = data["documentChange"]["document"]["fields"]["current_value"]["doubleValue"]
                            min_value = data["documentChange"]["document"]["fields"]["min_8_days"]["doubleValue"]
                            average_value = data["documentChange"]["document"]["fields"]["avg_8_days"]["doubleValue"]
                            max_value = data["documentChange"]["document"]["fields"]["max_8_days"]["doubleValue"]
                            print ("#####Site : "+site+"#####\nID : "+id+"\nCurrent : "+str(current_value)+"\nMin : "+str(min_value)+"\nAverage : "+str(average_value)+"\nMax : "+str(max_value)+"\n")
        last = output.find("["+str(i))

        
        
        
    #list_debut.append(debut)

#for i in range(len(list_debut)):
    #debut = list_debut[i]
    #fin = output[:list_debut[i+1]].rfind("]]")+2

    #print ("\n\n\n\n\n\n"+output[debut:fin])


#data = json.loads(output)

#for d in data:
    #print(d)