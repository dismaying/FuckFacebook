import argparse
import requests
from bs4 import BeautifulSoup
from terminaltables import SingleTable
import sys
from colorama import Fore, Style

# Importer la fonction display_banner depuis le fichier banner.py
from static.banner import display_banner

# Afficher la bannière avec les couleurs
print(Fore.RED + display_banner() + Style.RESET_ALL)

# Parser pour les arguments de ligne de commande
parser = argparse.ArgumentParser(description='Tool For Search information From dump facebook')
parser.add_argument('-i', '--id', help='ID')
parser.add_argument('-f', '--firstname', help='firstname')
parser.add_argument('-l', '--lastname', help='lastname')
parser.add_argument('-t', '--phone', help='phone')
parser.add_argument('-w', '--work', help='work')
parser.add_argument('-o', '--location', help='location')
args = parser.parse_args()

# Vérifier si aucun argument n'a été fourni
if not any(vars(args).values()):
    parser.print_help()
    sys.exit(1)

# Construire les paramètres de recherche pour l'URL
params = {
    'i': args.id if args.id else '',
    'f': args.firstname if args.firstname else '',
    'l': args.lastname if args.lastname else '',
    't': args.phone if args.phone else '',
    'w': args.work if args.work else '',
    'o': args.location if args.location else ''
}

# Filtrer les paramètres vides
filtered_params = {key: value for key, value in params.items() if value}

# Construire l'URL de recherche avec les paramètres filtrés
search_url = "http://4wbwa6vcpvcr3vvf4qkhppgy56urmjcj2vagu2iqgp3z656xcmfdbiqd.onion.pet/search?" + "&".join(f"{key}={value}" for key, value in filtered_params.items())

# Ajouter les paramètres fixes à l'URL de recherche
search_url += "&s=991004632&r=*any*&g=*any*"

# Effectuer la requête de recherche
response = requests.get(search_url)

# Traiter la réponse avec BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')

if table:
    # Extraire les données du tableau
    headers = [th.text.strip() for th in table.find_all('th')]
    data = []
    for row in table.find_all('tr')[1:]:
        row_data = [td.text.strip() for td in row.find_all('td')]
        data.append(row_data)

    # Créer un objet SingleTable avec les en-têtes et les données
    table_instance = SingleTable([headers] + data)

    # Rendre le tableau adaptatif en fonction de la taille du terminal
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    table_instance.justify_columns = {index: 'center' for index in range(len(headers))}

    # Afficher le tableau
    print(table_instance.table)
else:
    print("No Results.")
