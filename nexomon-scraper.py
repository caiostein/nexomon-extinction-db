import json
import requests
from bs4 import BeautifulSoup

# Function to scrape individual Nexomon page
def scrape_nexomon_details(nexomon_url):
    response = requests.get(nexomon_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Nexomon Name and Number
    title = soup.find('h2', class_='pi-title').get_text()

    number = title.split()[0]
    name = title.split()[2]

    # Sprites
    regular_sprite = soup.find('img', alt='Regular')['src']
    cosmic_sprite = soup.find('img', alt='Cosmic')['src']

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
        'name': food.find('img')['alt'],
        'image': food.find('img')['data-src']
    } 
    for food in soup.find_all('div', {'data-source': lambda x: x and 'food' in x})
]

    # Locations
    locations = scrape_table(soup, 'Locations')

    # Evolutions
    evolutions = scrape_table(soup, 'Evolution')

    #Skill Tree

    skill_tree = scrape_table(soup, 'Skill_Tree')

    # Output all collected data
    nexomon_data = {
        'Number': number,
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

# Example: Scraping the Cloddy page
nexomon_url = input('Input Nexomon Wiki Url: ') or 'https://nexomon.fandom.com/wiki/Cloddy'
nexomon_data = scrape_nexomon_details(nexomon_url)
file_name = nexomon_url.split('/')[-1]

# Export extracted data to JSON file
with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
    json.dump(nexomon_data, json_file, ensure_ascii=False, indent=4)  # Write to JSON
