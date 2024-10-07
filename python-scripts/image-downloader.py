import json
import requests
import re
import os

def download_image(url, save_path):
    try:
        # Check if the file already exists
        if os.path.exists(save_path):
            print(f"Image already exists, skipping: {save_path}")
            return
        
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the image
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded: {save_path}")
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")

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

        # Recursively search for image URLs in the JSON data
        def find_images_in_json(data, key_path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    find_images_in_json(value, f"{key_path}/{key}" if key_path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    find_images_in_json(item, f"{key_path}[{i}]")
            elif isinstance(data, str):
                # Check if the value is a URL that matches the pattern
                if image_url_pattern.match(data):
                    # Extract the image file name and download
                    file_name = os.path.basename(data)
                    save_path = os.path.join(download_dir, file_name)
                    download_image(data, save_path)
        
        # Start searching for images in the JSON file
        find_images_in_json(data)

    except Exception as e:
        print(f"Error while processing the JSON file: {e}")

# Example usage:
json_file_path = './assets/nexomon_extinction_database.json'  # Replace with your JSON file path
download_dir = 'downloaded_images'         # Directory to save the downloaded images
find_and_download_images(json_file_path, download_dir)
