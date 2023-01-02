# Scr4p
Repo de scraping des sites `cartoradio.fr` et `anfr.fr`.

## Pré-requis
- Python 3
- pyenv
- Les packages python contenu dans `requirements.txt`
```bash
pip install -r requirements.txt
```


## Création d'un venv python
```bash
python -m venv venv

#pyenv virtualenv 3.9 venv

source venv/bin/activate # Use this command on bash
.\venv\Scripts\activate # On Windows
pip install -r requirements.txt
```

## Usage 
### Cartoradio

```
# anciennete va rechercher des mesures sur les X derniers jours
python3 cartoradio/get_reports.py --anciennete 360   
```

### Observatoire des ondes

Le jeu de données en input doit absolument avoir le même format que celui en exemple `./observatoire\ des\ ondes/jeu_de_donnees_initial.xlsx`.
```
python3 ./observatoire\ des\ ondes/get_capteurs.py

Jeu de données initial (tapez juste entrée pour ignorer) : jeu_de_donnees_initial.xlsx

Année à extraire (tapez juste entrée pour extraire toutes les valeurs) : 2022
```
