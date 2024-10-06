import json
import re
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import unquote
from pathlib import Path

# Function to scrape individual Nexomon page
def scrape_nexomon_details(nexomon_url):

    print(nexomon_url)

    response = requests.get(nexomon_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Nexomon Name and Number
    title = soup.find('h2', class_='pi-title').get_text()

    number = title.split()[0].strip('#')
    nexomon_name = title.split()[2]

    # Sprites
    regular_sprite = soup.find('img', alt='Regular')['src'] if soup.find('img', alt='Regular') else next((img['src'] for img in soup.find_all('img') if nexomon_name in img['alt'] and "menu" not in img['alt']), None) 
    cosmic_sprite = soup.find('img', alt='Cosmic')['src'] if soup.find('img', alt='Cosmic') else None
    thumbnail = soup.find('img', alt=f'{nexomon_name}-menu')['data-src'] if soup.find('img', alt=f'{nexomon_name}-menu') else next((img['data-src'] for img in soup.find_all('img') if nexomon_name in img['alt'] and "menu" in img['alt']), None)

    # Element and Rarity
    element = soup.find('td', {'data-source': 'element'}).get_text(strip=True)
    element = element[:len(element) // 2]

    rarity = soup.find('td', {'data-source': 'rarity'}).get_text(strip=True)

    # Base Stats
    hp = soup.find('div', {'data-source': 'hp'}).get_text(strip=True)
    stamina = soup.find('div', {'data-source': 'stamina'}).get_text(strip=True)
    attack = soup.find('div', {'data-source': 'attack'}).get_text(strip=True)
    defense = soup.find('div', {'data-source': 'defense'}).get_text(strip=True)
    speed = soup.find('div', {'data-source': 'speed'}).get_text(strip=True)

    # Base Stats Total (BST)
    bst = soup.find('td', {'data-source': 'BST'}).get_text(strip=True)

    # Loved Food
    food_items = [
    {
        'name': food.find('img')['alt'] if food.find('img') else None,
        'image': food.find('img')['data-src'] if food.find('img') else None
    } 
    for food in soup.find_all('div', {'data-source': lambda x: x and 'food' in x})
]

    # Locations
    locations = scrape_table(soup, 'Locations')

    # Evolutions
    evolutions = scrape_table(soup, 'Evolution')

    #Skill Tree

    skill_tree = scrape_table(soup, 'Skill_Tree', 'Skills', 'Skill_List')

    # Output all collected data
    nexomon_data = {
        'Number': number,
        'Name': nexomon_name,
        'Sprites': {'Regular': regular_sprite, 'Cosmic': cosmic_sprite, 'Thumbnail': thumbnail},
        'Element': element,
        'Rarity': rarity,
        'Stats': {'HP': hp, 'Stamina': stamina, 'Attack': attack, 'Defense': defense, 'Speed': speed},
        'BST': bst,
        'Loved Food': food_items,
        'Locations': locations,
        'Evolution': evolutions,
        'Skill Tree': skill_tree
    }

    return nexomon_data

def scrape_table(soup, *span_ids):

    # Loop through the provided span IDs and stop when a valid table is found
    for span_id in span_ids:
        header = soup.find('span', {'id': span_id})
        if header:
            table = header.parent.find_next('table', {'class': 'wikitable'})
            if table:
                break  # Stop searching if a valid table is found

    # Extract the header row for the column names
    headers = []
    for th in table.find_all('th'):
       header_text = th.text.strip()
       colspan = int(th.get('colspan', 1))  # Get the colspan if present, default to 1
       headers.append({'header': header_text, 'colspan': colspan})

    # Extract the rows from the table
    rows = table.find_all('tr')[1:]  # Skip the header row

    table_data = []

    for row in rows:
        # Extract the values for each column
        columns = []
        for td in row.find_all('td'):
            # Check if the column has an image
            img = td.find('img')
            if img:
                # Extract image URL
                img_url = img['data-src']
                columns.append({'text': td.text.strip(), 'image': img_url})
            else:
                # Extract only text if no image
                columns.append(td.text.strip())

        # Create a dictionary using the headers and corresponding column values
        known = False
        row_data = {}

        for i in range(len(headers)):
            if headers[i]['colspan'] == 2:                
                row_data[headers[i]['header']] = columns[i]
                row_data[headers[i]['header']]['text'] = columns[i+1]
                known = True
            elif known:
                row_data[headers[i]['header']] = columns[i+1]
            else:
                row_data[headers[i]['header']] = columns[i]

        table_data.append(row_data)

    return table_data

# Clean .csv url
def clean_url(url):
    # Decode any URL encoding like %20 to spaces
    decoded_url = unquote(url)

    # Remove everything after the first space or quote character
    cleaned_url = decoded_url.split(' ')[0].split('"')[0]

    if cleaned_url.endswith('_/'):
        cleaned_url = cleaned_url.replace('_/', '_(Extinction)')
        

    
    return cleaned_url

# Function to process each URL
def process_nexomon_csv(file_path):
    all_nexomon_data = []

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Loop through each row in the CSV
        for row in reader:
            nexomon_url = clean_url(row['Nexomon Page Url'])
            
            # Call the scraper function for each URL
            nexomon_data = scrape_nexomon_details(nexomon_url)

            # Add latest data to database
            all_nexomon_data.append(nexomon_data)
    
    file_name = "nexomon_dirty_database"

    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_nexomon_data, json_file, ensure_ascii=False)      


# Define the function to clean URLs
def clean_image_url(url):
    return re.sub(r'(\.png).*', r'\1', url)

# Function to recursively clean URLs in a JSON object
def clean_urls_in_json(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value.startswith("http") and ".png" in value:
                data[key] = clean_image_url(value)
            else:
                clean_urls_in_json(value)
    elif isinstance(data, list):
        for item in data:
            clean_urls_in_json(item)

def process_json_image_urls(json_file_path):

    # Load your JSON file
    with open(json_file_path, 'r') as file:
        nexomon_data = json.load(file)

    # Clean all URLs in the JSON data
    clean_urls_in_json(nexomon_data)

    # Save the cleaned JSON back to a file
    with open('nexomon_extinction_database.json', 'w') as file:
        json.dump(nexomon_data, file, ensure_ascii=False)

def delete_file(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        file_path.unlink()
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")

# Scrapes Nexomon Wiki for information
process_nexomon_csv('./assets/names_and_thumbnails.csv')

# Cleans Image Urls
process_json_image_urls('./assets/nexomon_dirty_database.json')

# Deletes old database file
delete_file('./assets/nexomon_dirty_database.json')




# def process_single_nexomon(nexomon_url):
#     nexomon_data = scrape_nexomon_details(nexomon_url)

#     file_name = "data"

#     with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
#          json.dump(nexomon_data, json_file, ensure_ascii=False, indent=4) 

#process_single_nexomon("https://nexomon.fandom.com/wiki/Venefelis")