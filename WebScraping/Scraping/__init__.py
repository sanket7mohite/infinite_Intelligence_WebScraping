import csv
import os
import time
from typing import Dict
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.infinite-intelligence.net'

driver = webdriver.Firefox()
driver.get(url)

########################### Scrap Entire Page Source ############################
time.sleep(5)
DOM = driver.page_source
with open('Page_Source/webpage_content.html', 'w', encoding='utf-8') as file:
    file.write(DOM)

########################### Downloading all the Images from img tag ############################
# List to store image filenames
image_data = []
# meta_description = []
# meta_viewport = []

count = 1
image_elements = driver.find_elements(By.TAG_NAME, "img")

for idx, img in enumerate(image_elements):
    img_url = img.get_attribute('src')
    # print(img_url)
    if img_url:
        # scode = img_response.status_code
        # print(f"status Code-> {scode}")
        # print(scode)
        actual_url = img_url
        parsed_url = urlparse(actual_url)
        corrected_netloc = parsed_url.netloc.replace('..', '.')
        path = f"{parsed_url.scheme}://{corrected_netloc}{parsed_url.path}"
        # print(path)

    img_response = requests.get(path)
    if img_response.status_code == 200:
        # print(f"URL is OK: {path}")
        img_name = os.path.join('Selenium_Downloaded_Images', os.path.join(os.path.basename(path)))
        file_name = os.path.join(os.path.basename(path))
        image_data.append({'Image_FileName': file_name})
        with open(img_name, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f"Downloaded: {img_name}")
    else:
        print(f"Something is wrong with image URL: {path}")

########################### Downloading all the Images from CSS background ############################
ele_list = driver.find_elements(By.TAG_NAME, "div")
for ele in ele_list:
    img_path = ele.value_of_css_property('background-image')
    # print(img_path)

    if 'https' in img_path:
        path = img_path.split('url("')[1].split('")')[0]
        # print(path)
        if path:
            actual_url = path
            parsed_url = urlparse(actual_url)
            corrected_netloc = parsed_url.netloc.replace('..', '.')
            path = f"{parsed_url.scheme}://{corrected_netloc}{parsed_url.path}"
            # print(path)

        img_response = requests.get(path)
        if img_response.status_code == 200:
            print(f"URL is OK: {path}")
            img_name = os.path.join('Selenium_Downloaded_Images', os.path.join(os.path.basename(path)))
            file_name = os.path.join(os.path.basename(path))
            image_data.append({'Image_FileName': file_name})
            with open(img_name, 'wb') as img_file:
                img_file.write(img_response.content)
            print(f"Downloaded: {img_name}")
        else:
            print(f"Something is wrong with image URL: {path}")

meta_description = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute('content')
print(meta_description)
meta_viewport = driver.find_element(By.XPATH, "//meta[@name='viewport']").get_attribute('content')
print(meta_viewport)

# Save image data to a CSV file

fieldnames = ['Image_FileName', 'meta_description', 'meta_viewport']
csv_filename = 'image_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(
        {'Image_FileName': image_data, 'meta_description': meta_description, 'meta_viewport': meta_viewport})
    # for data in image_data:
    #     writer.writerow(data)

########################### Parsing the Text from the Page ############################
driver.save_full_page_screenshot('ScreenShots/ScreenShot.png')
driver.quit()
