import requests
import json

url = "https://data.anfr.fr/api/datasets/2.0/DATASETID/id=mesures-sondes-autonomes"

response = requests.get(url)

outjson = json.loads(response.text)

for i in outjson["result"]["extras"]:
    if i["key"] == "file_csv":
        url = i["value"]


response = requests.get(url)
output = response.text

ligne = output.split("\n")

already = []
for li in ligne:
    if len(li.split(";")) > 6:
        name = li.split(";")[6]
        if name not in already and name != "numero":
            already.append(name)

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Host': 'data.nantesmetropole.fr', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15', 'Accept-Language': 'fr-FR,fr;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}
url = "https://data.nantesmetropole.fr/api/records/1.0/search/?dataset=244400404_capteurs-ondes-electomagnetiques-nantes-metropole&q=&sort=extractjson_date&facet=name&facet=address"

response = requests.get(url, headers = headers)

outjson = json.loads(response.text)

for records in outjson["facet_groups"]:
    for facets in records["facets"]:
        if facets["name"].startswith("Nantes"):
            if facets["name"] not in already and facets["name"] != "name":
                already.append(facets["name"])

print(already)
