#!/usr/bin/env python
# coding: utf-8

import pandas as pd

print('---- Getting financing by projects by category by country ------')
# Import the ai-investment-and-financing-projects-by-category-country.xlsx
funCategCountry = pd.ExcelFile('ai-investment-and-financing-projects-by-category-country.xlsx')
# Create the dataframe from the second sheet and skip the first 4 rows to get the data
funCategCountry_df = funCategCountry.parse('Data', skiprows=4, usecols="B:L")
# Rename the first row to Country
funCategCountry_df.rename(columns={'Unnamed: 1':'Country'}, inplace=True)
# Get the countries list
country_list1 = funCategCountry_df['Country'].tolist()

print('---- Getting financing by share by country ------')
# Import the ai-investment-and-financing-share-by-country-2013-2018.xlsx
funCountryShare = pd.ExcelFile('ai-investment-and-financing-share-by-country-2013-2018.xlsx')
# Create the dataframe from the second sheet and skip the first 4 rows to get the data
funCountryShare_df = funCountryShare.parse('Data', skiprows=4, usecols="B:C")
# Rename the first row to Country
funCountryShare_df.rename(columns={'Unnamed: 1':'Country'}, inplace=True)
# Get the countries list
country_list2 = funCountryShare_df['Country'].tolist()

print('---- Getting AI professionals by country ------')
# Import the ai-investment-and-financing-share-by-country-2013-2018.xlsx
AIprofCountry = pd.ExcelFile('ai-professionals-by-country-worldwide-2017.xlsx')
# Create the dataframe from the second sheet and skip the first 4 rows to get the data
AIprofCountry_df = AIprofCountry.parse('Data', skiprows=4, usecols="B:C")
# Rename the first row to Country
AIprofCountry_df.rename(columns={'Unnamed: 1':'Country'}, inplace=True)
# Get the countries list
country_list3 = AIprofCountry_df['Country'].tolist()

print('---- Getting AI related papers by country ------')
# Import the ai-investment-and-financing-share-by-country-2013-2018.xlsx
AIpaperCountry = pd.ExcelFile('ai-related-paper-publications-worldwide-by-country.xlsx')
# Create the dataframe from the second sheet and skip the first 4 rows to get the data
AIpaperCountry_df = AIpaperCountry.parse('Data', skiprows=4, usecols="B:C")
# Rename the first row to Country
AIpaperCountry_df.rename(columns={'Unnamed: 1':'Country'}, inplace=True)
# Get the countries list
country_list4 = AIpaperCountry_df['Country'].tolist()

print('---- Getting the common countries list ------')
# Get the common countries list
final_countries = set(country_list1).intersection(country_list2).intersection(country_list3).intersection(country_list4)

print('---- Retrieving common country indexes for each dataframe ------')
# Retrieve the indexes of countries of the common countries in funds by category dataframe
categfilter = [True if i in final_countries else False for i in funCategCountry_df['Country'].tolist()]
# Retrieve the indexes of countries of the common countries in funds by share dataframe
sharefilter = [True if i in final_countries else False for i in funCountryShare_df['Country'].tolist()]
# Retrieve the indexes of countries of the common countries in professional by country dataframe
proffilter = [True if i in final_countries else False for i in AIprofCountry_df['Country'].tolist()]
# Retrieve the indexes of countries of the common countries in paper publications by country dataframe
paperfilter = [True if i in final_countries else False for i in AIpaperCountry_df['Country'].tolist()]

print('---- Reading startup by country data ------')
# Get the startups by country from startups.csv
startupCountry_df = pd.read_csv('startup_per_country.csv')
# Retrieve the indexes of countries of the common countries in startups by country dataframe
startupfilter = [True if i in final_countries else False for i in startupCountry_df['Country'].tolist()]

print('----- Writing to CSVs -----------')
# Write the new CSVs with common countries
funCategCountry_df[categfilter].to_csv('CategoryCountry.csv')
funCountryShare_df[sharefilter].to_csv('ShareCountry.csv')
AIprofCountry_df[proffilter].to_csv('ProffesionalsCountry.csv')
AIpaperCountry_df[paperfilter].to_csv('PaperCountry.csv')
startupCountry_df[startupfilter].to_csv('Startup.csv', columns=['Country',',No of startups'])