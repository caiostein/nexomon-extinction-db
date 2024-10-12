import json
import re
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import unquote
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to scrape individual Nexomon page
def scrape_nexomon_details(nexomon_url):

    print(f"Scraping: {nexomon_url}")

    response = requests.get(nexomon_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Nexomon Name and Number
    title = soup.find('h2', class_='pi-title').get_text()

    number = title.split()[0].strip('#')
    nexomon_name = title.split()[2]

    # Description code
    description_header = soup.find('span', {'id': 'Description'})
    if description_header:
        # The next sibling to <h2> or <span> is typically a <p> tag containing the description
        nexomon_description = description_header.find_parent('h2').find_next('p').get_text(strip=True)
    else:
        nexomon_description = "Description not found"

    # Output all collected data
    nexomon_data = {
        'Number': number,
        'Name': nexomon_name,
        'Description': nexomon_description
    }

    return nexomon_data

# Clean .csv url
def clean_url(url):
    # Decode any URL encoding like %20 to spaces
    decoded_url = unquote(url)

    # Remove everything after the first space or quote character
    cleaned_url = decoded_url.split(' ')[0].split('"')[0]

    if cleaned_url.endswith('_/'):
        cleaned_url = cleaned_url.replace('_/', '_(Extinction)')
    
    return cleaned_url

# Function to scrape data concurrently
def process_nexomon_csv(file_path):
    all_nexomon_data = []
    urls = []

    # Read URLs from CSV
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nexomon_url = clean_url(row['Nexomon Page Url'])
            urls.append(nexomon_url)

    # Use ThreadPoolExecutor to scrape in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:  # You can adjust the number of workers based on your system
        futures = {executor.submit(scrape_nexomon_details, url): url for url in urls}

        for future in as_completed(futures):
            try:
                nexomon_data = future.result()
                all_nexomon_data.append(nexomon_data)
            except Exception as e:
                print(f"Error scraping {futures[future]}: {e}")

    # Save the results to JSON
    file_name = "nexomon_description_database"
    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_nexomon_data, json_file, ensure_ascii=False)

# Scrapes Nexomon Wiki for information
process_nexomon_csv('./assets/names_and_thumbnails.csv')



# def process_single_nexomon(nexomon_url):
#     nexomon_data = scrape_nexomon_details(nexomon_url)

#     file_name = "data"

#     with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
#          json.dump(nexomon_data, json_file, ensure_ascii=False, indent=4) 

# process_single_nexomon("https://nexomon.fandom.com/wiki/Cloddy")