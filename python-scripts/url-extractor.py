import re
import json

# Define the regex pattern to match the URL up to the .png
url_pattern = r'(https?://[^\)]+?\.png)'

# Function to extract URLs from a CSV file
def extract_urls_from_csv(file_path):
    urls = []

    # Open and read the CSV file
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(url_pattern, line)
            if match:
                urls.append(match.group(1))  # Append the extracted URL to the list

    return urls

# Function to write URLs to a JSON file
def write_urls_to_json(urls, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(urls, json_file, indent=4)

# Specify the path to your CSV file and output JSON file
csv_file_path = './assets/LocationInfo.csv'
json_file_path = './assets/urls.json'

# Call the functions
extracted_urls = extract_urls_from_csv(csv_file_path)
write_urls_to_json(extracted_urls, json_file_path)

print(f"Extracted URLs have been written to {json_file_path}")