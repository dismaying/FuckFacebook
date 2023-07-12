import argparse
import requests
from bs4 import BeautifulSoup
from terminaltables import SingleTable
import sys
from colorama import Fore, Style

# Import the display_banner function from the banner.py file
from static.banner import display_banner

# Display the banner with colors
print(Fore.RED + display_banner() + Style.RESET_ALL)

# Parser for command line arguments
parser = argparse.ArgumentParser(description='Tool For Search information From dump facebook')
parser.add_argument('-i', '--id', help='ID')
parser.add_argument('-f', '--firstname', help='firstname')
parser.add_argument('-l', '--lastname', help='lastname')
parser.add_argument('-t', '--phone', help='phone')
parser.add_argument('-w', '--work', help='work')
parser.add_argument('-o', '--location', help='location')
args = parser.parse_args()

# Check if no arguments were provided
if not any(vars(args).values()):
    parser.print_help()
    sys.exit(1)

# Build the search parameters for the URL
params = {
    'i': args.id if args.id else '',
    'f': args.firstname if args.firstname else '',
    'l': args.lastname if args.lastname else '',
    't': args.phone if args.phone else '',
    'w': args.work if args.work else '',
    'o': args.location if args.location else ''
}

# Filter out empty parameters
filtered_params = {key: value for key, value in params.items() if value}

# Build the search URL with the filtered parameters
search_url = "http://4wbwa6vcpvcr3vvf4qkhppgy56urmjcj2vagu2iqgp3z656xcmfdbiqd.onion.pet/search?" + "&".join(f"{key}={value}" for key, value in filtered_params.items())

# Add the fixed parameters to the search URL
search_url += "&s=991004632&r=*any*&g=*any*"

# Perform the search request
response = requests.get(search_url)

# Process the response with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')

if table:
    # Extract the data from the table
    headers = [th.text.strip() for th in table.find_all('th')]
    data = []
    for row in table.find_all('tr')[1:]:
        row_data = [td.text.strip() for td in row.find_all('td')]
        data.append(row_data)

    # Create a SingleTable object with the headers and data
    table_instance = SingleTable([headers] + data)

    # Make the table responsive based on the terminal size
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    table_instance.justify_columns = {index: 'center' for index in range(len(headers))}

    # Display the table
    print(table_instance.table)
else:
    print("No Results.")
