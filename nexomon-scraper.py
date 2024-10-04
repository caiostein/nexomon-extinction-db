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
    locations = scrape_locations(soup)

    # Output all collected data
    nexomon_data = {
        'Name': name,
        'Sprites': {'Regular': regular_sprite, 'Cosmic': cosmic_sprite},
        'Element': element,
        'Rarity': rarity,
        'Stats': {'HP': hp, 'Stamina': stamina, 'Attack': attack, 'Defense': defense, 'Speed': speed},
        'BST': bst,
        'Loved Food': food_items,
        'Locations': locations
    }

    return nexomon_data

def scrape_locations(soup):
    # Find the span element with id 'Locations'
    locations_header = soup.find('span', {'id': 'Locations'}).parent

    # Find the first table that follows the 'Locations' h2 element
    location_table = locations_header.find_next('table', {'class': 'wikitable'})

    # Extract rows from the table
    rows = location_table.find_all('tr')[1:]  # Skip the header row

    nexomon_locations = []

    for row in rows:
        # Extract the region
        region = row.find_all('td')[0].text.strip()

        # Extract the maps, splitting by commas
        maps = row.find_all('td')[1].text.strip().split(", ")

        nexomon_locations.append({
            'Region': region,
            'Maps': maps
        })
    return nexomon_locations

# Example: Scraping the Cloddy page
nexomon_url = 'https://nexomon.fandom.com/wiki/Cloddy'
cloddy_data = scrape_nexomon_details(nexomon_url)

# Print extracted data
print(cloddy_data)
