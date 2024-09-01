import requests #Used to fetch the contents of the URL.
import zipfile #Used to handle zip files, both for extraction and creation.
import os #Provides functionalities to interact with the operating system, such as file operations and path manipulation.
import shutil

from bs4 import BeautifulSoup as bs
url='https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets'
res=requests.get(url)   # sending request to the link
soup=bs(res.text, 'html.parser')
#file_type='.zip'
years_list=['2023','2022']
final_years_list=[]
for years in years_list:
    year_latest=years + '_latest.zip'
    final_years_list.append(year_latest)
    year_Latest=years + '_Latest.zip'
    final_years_list.append(year_Latest)

print(final_years_list)#keywords to download desired files
zip_file_links=[]
for sp in soup.find_all('div',class_='field field--name-field-p-accordion-body field--type-text-long field--label-hidden clearfix'):
    for link in sp.find_all('a'):
        file_link=link.get('href')
        for year in final_years_list:
            if year in file_link:
                zip_file_links.append(file_link)

# Function to download and unzip a file
def download_and_unzip(url, download_folder, extract_folder):
    # Create the download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Fetch the zip file
    zip_response = requests.get(url)

    # Save the zip file to the download folder
    zip_file_path = os.path.join(download_folder, os.path.basename(url))
    with open(zip_file_path, 'wb') as f:
        f.write(zip_response.content)

    print(f"Downloaded zip file saved at: {zip_file_path}")

    # Create the extraction folder if it doesn't exist
    os.makedirs(extract_folder, exist_ok=True)

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    print(f"Extracted contents saved at: {extract_folder}")

    # Optionally, you can delete the downloaded zip file after extraction
    #os.remove(zip_file_path)
# Function to clear contents of a folder
def clear_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder) #to recursively delete all files and folders in folder
    os.makedirs(folder) #recreates the folder using os.makedirs(folder).
# Example usage:

# Define longer paths for download and extraction
base_folder = '/Users/cookie/Documents/web_scraping/downloading_files/'
download_folder = os.path.join(base_folder, 'zip_downloads')
extract_folder = os.path.join(base_folder, 'zip_extracted')

clear_folder(download_folder)
clear_folder(extract_folder)
# List of URLs of the zip files you want to download and extract

# Loop through each URL and download/unzip
for url in zip_file_links:
    download_and_unzip(url, download_folder, extract_folder)

