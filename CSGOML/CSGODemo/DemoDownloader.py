import os
import urllib.request
import gzip
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Path to the file containing the links
links_file_path = 'demos.txt'

# Directory to save downloaded and extracted files
output_directory = "C:/Users/S_CSIS-PostGrad/Documents/Honours/Project/MLMatchMaker/CSGODemo/demos"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Define a custom user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def download_and_extract(index, line):
    parts = line.strip().split(',')
    if len(parts) == 2:
        url = parts[1].split('-', 1)[1]
        output_filename = url.split('/')[-1]
        downloaded_path = os.path.join(output_directory, output_filename)

        print(f"Downloading file {index}/{total_lines}: {url}")
        headers = {'User-Agent': user_agent}
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response, open(downloaded_path, 'wb') as out_file:
            out_file.write(response.read())

        # Extract the downloaded gz file
        extracted_filename = output_filename.replace('.gz', '')
        extracted_path = os.path.join(output_directory, extracted_filename)
        with open(downloaded_path, 'rb') as gz_file, open(extracted_path, 'wb') as out_file:
            with gzip.GzipFile(fileobj=gz_file) as gz:
                out_file.write(gz.read())

        # Remove the downloaded gz file
        os.remove(downloaded_path)

        print(f"Downloaded and extracted: {extracted_filename}")

# Read the links from the file and process each line using multithreading
with open(links_file_path, 'r') as file:
    lines = file.readlines()
    total_lines = len(lines)

    with ThreadPoolExecutor(max_workers=12) as executor:  # Adjust max_workers as needed
        futures = [executor.submit(download_and_extract, index, line) for index, line in enumerate(lines, start=1)]
        for future in tqdm(futures, total=total_lines, desc="Progress"):
            future.result()

print("All files downloaded and extracted.")