import requests
import string
import random
import json
import datetime
import base64
import openpyxl
import pandas as pd

#df = pd.read_excel ('/Users/mathiasguillemot/Documents/GitHub/scr4p/jeu_de_donnees_initial.xlsx', 'Sheet1')
df = pd.read_excel ('/Users/mathiasguillemot/Documents/GitHub/scr4p/jeu_de_donnees_initial.xlsx')

df2 = df

print (df2[id][0])

#wb = openpyxl.load_workbook(filename = '/Users/mathiasguillemot/Documents/GitHub/scr4p/jeu_de_donnees_initial.xlsx')
#sheet_ranges = wb['Sheet1']

#sheet_ranges['A2'] = 'hello world'

#wb.save('/Users/mathiasguillemot/Documents/GitHub/scr4p/text.xlsx')