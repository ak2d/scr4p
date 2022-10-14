from PyPDF2 import PdfFileReader

fichier = PdfFileReader('RPUB_150497.pdf')
signets = fichier.outline

def check_is_mesure_exist(o):
    for i in o:
        if isinstance(i, list):
            is_exist = check_is_mesure_exist(i)
        else:
            if i.title == "Résultat de la mesure spécifique*":
                return i.page
        if 'is_exist' in locals() and is_exist != None:
            return is_exist
                
        


if check_is_mesure_exist(signets) != None:
    print("WWWWWwwOOOOOOOOOOO")