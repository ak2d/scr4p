from PyPDF2 import PdfFileReader

fichier = PdfFileReader('cartoradio/RPUB_150497.pdf')
signets = fichier.outline

def check_is_mesure_exist(o):
    for i in o:
        if isinstance(i, list):
            is_exist = check_is_mesure_exist(i)
        else:
            if i.title == "Résultat de la mesure spécifique*":
                
                return i
        if 'is_exist' in locals() and is_exist != None:
            return is_exist
                
        

is_mesure_exist=check_is_mesure_exist(signets)
if is_mesure_exist != None:
    print("WWWWWwwOOOOOOOOOOO")

    print(type(is_mesure_exist))
    npage=fichier.get_destination_page_number(is_mesure_exist)
    print(type(npage))
    print(npage)
    page=fichier.getPage(npage)

    print(type(page.get_contents()))
    print(page.get_contents())

    txt=page.extractText()
    # txt.replace('\x13 e', 'é')
    # txt.replace('\x13E', 'É')
    # txt.replace('\x12 a', 'à')
    # txt.replace('\x12 e', 'è')
    # txt.replace('\'', "'")
    # txt.replace('\\', '"')
    # txt.replace('\\x0', 'f')
    print(type(txt))
    print(txt)

    

    print("wowowo")