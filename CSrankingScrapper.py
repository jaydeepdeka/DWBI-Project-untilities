#!/usr/bin/env python
# coding: utf-8
'''
Scrap CSRanking.org for college info
author: jdeka
v0.1
date: 02-Mar-2019
'''
import csv
import json
import pandas as pd
import pickle
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


# Google Geo API key and Chromedriver
API_KEY = r''####
driver = webdriver.Chrome(r'D:\Chromedriver\chromedriver')
geomap_path = r'https://maps.googleapis.com/maps/api/geocode/json?address={},+CA&key={}'
# URL of the page
quote_page = 'http://csrankings.org/#/index?ai&vision&mlmining&nlp&ir&world'
driver.get(quote_page)
# Wait for the page to load
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Close the browser
driver.quit()
# Find the ranking table
table = soup.find('table', attrs={'id':'ranking'})
trs = table.find('tbody').find_all('tr',recursive=False)
# The name of the universities occurs every 3rd row
row_list = []
print('Starting info retreiving: ')
# count = 0

# Get the countries list object to be used to remove universties of countries not required
with open('final_countries.set', 'rb') as final_countries:
	country_list = pickle.load(final_countries)

abbrv = {'USA':'United States', 'UK':'United Kingdom'}
for i, idx in enumerate(range(0,len(trs),3)):
    # Append with the ranking
    desc_list = [i+1]
    for j, td in enumerate(trs[idx].findAll('td')):
        # print(type(td.get_text()))
        if j==1:
            # To remove some special character in the university names
            splitted_text = td.get_text().strip().split()[1:]
            univ_name = ' '.join(splitted_text)
            print('Univ name: {} retrieved from CSRankings.org'.format(univ_name))
            # Append the university name to the list
            desc_list.append(univ_name)
            # Build the url path
            url = geomap_path.format('+'.join(splitted_text), API_KEY)
            # Get the content
            print('Getting location data for {} from Google maps'.format(univ_name))
            response = requests.get(url)
            json_text = response.text
            parsed = json.loads(json_text)
            if not parsed['results']:
                break
            # The output is of format "formatted_address" : "1280 Main St W, Hamilton, ON L8S 4L8, Canada"
            # Split the strip and get the last element for the country
            # country = parsed["results"][0]["formatted_address"].split(',')[-1].strip()
            country = parsed["results"][0]["formatted_address"].strip()
            # The resulted address contains abbreviations for the US and UK, replace with full name
            if 'USA' in country:
                country = country.replace('USA', 'United States')
            if 'UK' in country:
                country = country.replace('UK', 'United Kingdom')
            # Don't enter the universities of countries which are not common
            found = False
            for country_name in country_list:
                if country_name in country:
                    country = country_name
                    found = True
                    break
                else:
                    continue
            if not found:
                break
            desc_list.append(country)
        else:
            desc_list.append(td.get_text().strip())
        # print(td.get_text())
    if len(desc_list) == 6:
        row_list.append(desc_list)
    else:
        continue
print('CSV  writing starts!!!!')
# Start writing to the CSV file
with open('university.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headings first
    writer.writerow(['Ranking', 'Matrix', 'University Name', 'Country', 'Publications', 'Faculty'])
    for row in row_list:
        writer.writerow(row)

print('CSV  writing done!!!!')
