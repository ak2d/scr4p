import requests
import string
import random
import json
import datetime
import base64
import matplotlib.pyplot
import matplotlib.dates

headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3","Connection": "keep-alive", "Host": "odo-prod.ey.r.appspot.com", "Origin": "https://www.observatoiredesondes.com", "Referer": "https://www.observatoiredesondes.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0"}

id = "00620af7-d292-4c0b-b633-c46365cfa6d9"
url = "https://odo-prod.ey.r.appspot.com/public_datas/"+id

r = requests.get(url, headers = headers)

output = base64.b64decode(r.text).decode()

data = json.loads(output)

x_values = []
y_values = []

for values in data["values"]:
    date = datetime.datetime.fromtimestamp(values["date"])
    value = values["value"]
    x_values.append(date)
    y_values.append(value)
    print (str(date)+" : "+str(value))

#dates = matplotlib.dates.date2num(x_values)
#matplotlib.pyplot.plot_date(dates, y_values)

matplotlib.pyplot.plot(x_values ,y_values)
#matplotlib.pyplot.scatter(x_values ,y_values)

matplotlib.pyplot.gcf().autofmt_xdate()

#myFmt = matplotlib.dates.DateFormatter('%H:%M')
#myFmt = matplotlib.dates.DateFormatter('%d')
#matplotlib.pyplot.gca().xaxis.set_major_formatter(myFmt)

matplotlib.pyplot.show()
