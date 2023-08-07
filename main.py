import argparse
import requests
from bs4 import BeautifulSoup
from terminaltables import SingleTable
import sys
from colorama import Fore, Style
from token_config import URL_TOKEN

# Import de la fonction display_banner depuis le fichier banner.py
from static.banner import display_banner

# Affichage de la bannière avec des couleurs
print(Fore.RED + display_banner() + Style.RESET_ALL)

def pass_the_captcha():

    url_index = "http://4wbwa6vcpvcr3vvf4qkhppgy56urmjcj2vagu2iqgp3z656xcmfdbiqd.onion.pet/"

    req = requests.get(url_index, verify=False)
    soup = BeautifulSoup(req.text, "html.parser")
    get_captcha = soup.find('pre').text
    get_id = soup.find('input', {'name': 'id'}).get('value')
    print(get_captcha)

    captcha = input("Entrez le captcha: ")
    url_captcha = "{}captcha".format(url_index)

    datas = {
        "captcha": captcha,
        "id": get_id
    }
    
    req_captcha = requests.post(url_captcha, verify=False, data=datas)
    with open("token_config.py", "w") as replace_token:
        replace_token.write("""URL_TOKEN = "{}" """.format(req_captcha.url.split("=")[-1]))
    main(req_captcha.url.split("=")[-1])

def main(URL_TOKEN):
    # Filtrage des paramètres vides
    filtered_params = {key: value for key, value in params.items() if value}

    # Construction de l'URL de recherche avec les paramètres filtrés
    search_url = "http://4wbwa6vcpvcr3vvf4qkhppgy56urmjcj2vagu2iqgp3z656xcmfdbiqd.onion.pet/search?" + "&".join(f"{key}={value}" for key, value in filtered_params.items())

    # Ajout des paramètres fixes à l'URL de recherche
    search_url += "&s={}&r=*any*&g=*any*".format(URL_TOKEN)

    # Effectuer la requête de recherche
    response = requests.get(search_url, verify=False, allow_redirects=True)

    # Traitement de la réponse avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    if "fill" in response.text:
        pass_the_captcha()
    else:

        table = soup.find('table')

        if table:
            # Extraction des données de la table
            headers = [th.text.strip() for th in table.find_all('th')]
            data = []
            for row in table.find_all('tr')[1:]:
                row_data = [td.text.strip() for td in row.find_all('td')]
                data.append(row_data)

            # Création d'un objet SingleTable avec les en-têtes et les données
            table_instance = SingleTable([headers] + data)

            # Rendre la table responsive en fonction de la taille du terminal
            table_instance.inner_heading_row_border = False
            table_instance.inner_row_border = True
            table_instance.justify_columns = {index: 'center' for index in range(len(headers))}

            # Affichage de la table
            print(table_instance.table)

            # Ajout d'un espace et d'un titre
            print("\nDirect Link to Facebook profile:\n")

            # Affichage des URL de profils Facebook en utilisant les ID de la table
            for row in data:
                fb_url = f"https://www.facebook.com/profile.php?id={row[0]}"
                print(fb_url)

        else:
            print("Aucun résultat.")

if __name__ == '__main__':

    # Analyseur pour les arguments de la ligne de commande
    parser = argparse.ArgumentParser(description='Outil pour rechercher des informations dans un dump Facebook')
    parser.add_argument('-i', '--id', help='ID')
    parser.add_argument('-f', '--firstname', help='prénom')
    parser.add_argument('-l', '--lastname', help='nom de famille')
    parser.add_argument('-t', '--phone', help='téléphone')
    parser.add_argument('-w', '--work', help='travail')
    parser.add_argument('-o', '--location', help='localisation')
    args = parser.parse_args()

    # Vérification si aucun argument n'a été fourni
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    # Construction des paramètres de recherche pour l'URL
    params = {
        'i': args.id if args.id else '',
        'f': args.firstname if args.firstname else '',
        'l': args.lastname if args.lastname else '',
        't': args.phone if args.phone else '',
        'w': args.work if args.work else '',
        'o': args.location if args.location else ''
    }
    main(URL_TOKEN)
