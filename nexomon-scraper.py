import json
import requests
from bs4 import BeautifulSoup

# Function to scrape individual Nexomon page
def scrape_nexomon_details(nexomon_url):
    response = requests.get(nexomon_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Nexomon Name
    name = soup.find('h2', class_='pi-title').get_text()

    # Sprites
    regular_sprite = soup.find('img', alt='Regular')['src']
    cosmic_sprite = soup.find('img', alt='Cosmic')['src']

    # Element and Rarity
    element = soup.find('td', {'data-source': 'element'}).get_text(strip=True)
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
    food_items = [food.find('img')['alt'] for food in soup.find_all('div', {'data-source': lambda x: x and 'food' in x})]

    # Locations
    locations = scrape_table(soup, 'Locations')

    # Evolutions
    evolutions = scrape_table(soup, 'Evolution')

    #Skill Tree

    skill_tree = scrape_table(soup, 'Skill_Tree')

    # Output all collected data
    nexomon_data = {
        'Name': name,
        'Sprites': {'Regular': regular_sprite, 'Cosmic': cosmic_sprite},
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

def scrape_table(soup, span_id):
    # Find the span element with the given ID
    header = soup.find('span', {'id': span_id}).parent

    # Find the first table that follows the header element
    table = header.find_next('table', {'class': 'wikitable'})

    # Extract the header row for the column names
    headers = [th.text.strip() for th in table.find_all('th')]

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
        row_data = {headers[i]: columns[i] for i in range(len(headers))}

        table_data.append(row_data)

    return table_data

# Example: Scraping the Cloddy page
nexomon_url = 'https://nexomon.fandom.com/wiki/Cloddy'
cloddy_data = scrape_nexomon_details(nexomon_url)

# Export extracted data to JSON file
with open('cloddy_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(cloddy_data, json_file, ensure_ascii=False, indent=4)  # Write to JSON

# Print extracted data
print(cloddy_data)
