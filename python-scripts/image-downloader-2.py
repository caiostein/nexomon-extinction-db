import json
from urllib.parse import unquote
import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_image(url, save_path):
    try:
        # Check if the file already exists
        if os.path.exists(save_path):
            print(f"Image already exists, skipping: {save_path}")
            return
        
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the image
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded: {save_path}")
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while downloading {url}: {e}")

def find_and_download_images(json_file_path, download_dir):
    try:
        # Load the JSON data
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Create download directory if it doesn't exist
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Define the regex pattern for the image URLs
        image_url_pattern = re.compile(r'^https.*\.png$')

        # Prepare a list to hold the download tasks
        download_tasks = []

        # Recursively search for image URLs in the JSON data
        def find_images_in_json(data):
            if isinstance(data, dict):
                for value in data.values():
                    find_images_in_json(value)
            elif isinstance(data, list):
                for item in data:
                    find_images_in_json(item)
            elif isinstance(data, str):
                # Check if the value is a URL that matches the pattern
                if image_url_pattern.match(data):
                    # Extract the image file name and prepare to download
                    #original_filename = data.split('/')[-8].split('/revision')[0]
                    file_name = unquote(os.path.basename(data))
                    save_path = os.path.join(download_dir, file_name)
                    download_tasks.append((data, save_path))
        
        # Start searching for images in the JSON file
        find_images_in_json(data)

        # Download images concurrently
        with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers based on your network capability
            future_to_url = {executor.submit(download_image, url, path): url for url, path in download_tasks}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Failed to download {url}: {e}")

    except Exception as e:
        print(f"Error while processing the JSON file: {e}")

# Example usage:
json_file_path = './assets/nexomon_extinction_database.json'  # Replace with your JSON file path
download_dir = './assets/downloaded_images'         # Directory to save the downloaded images
find_and_download_images(json_file_path, download_dir)
