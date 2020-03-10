#!/bin/python3
"""
COVID-19 webscraper for USA.

created by AUcod3r on 9 March 2020

Uses the site https://www.worldometers.info/coronavirus/country/us/
to track infections and dispositions in the USA
"""
from bs4 import BeautifulSoup
import requests
import datetime as dt
import os


def writeData():
    """
    Append the data to covidData.txt.

    Keeps track of daily activity and deltas.
    """
    with open('covidData.txt', 'a') as f:
        f.write(
            f'{today} - USA COVID-19 cases today: {values[0]} - Active cases:'
            f' {values[3]} - Closed cases: {values[4]} - Recovered: '
            f'{values[2]} - Deaths: {values[1]}\n')


# Grab the source and keep this assignment under 80 chars
html_source = (requests.get
               ('https://www.worldometers.info/coronavirus/country/us/').text)

# Create the BeautifulSoup object from the source code
soup = BeautifulSoup(html_source, 'lxml')

today = dt.datetime.today().strftime("%A, %d %B %Y")

# Print to the terminal
print(
    "\n************* United States of America COVID-19 Data ***************\n")
print("Today's date:", today)
# Create 2 empty lists to grab the data from the soup object
labels = []
values = []
# Grab the labels and values from the appropriate divs
for headline in soup.find_all('div', id='maincounter-wrap'):
    labels.append(headline.h1.text)
    values.append(headline.find(class_='maincounter-number').text)
# Grab the labels and values from the appropriate divs
for cases in soup.find_all('div', class_='col-md-6'):
    labels.append(cases.find(class_='panel-heading').text)
    values.append(cases.find(class_='number-table-main').text)
# Print to the terminal
for i in range(len(labels)):
    print(labels[i], values[i])
# Call the function to write today's data
writeData()
# Print a nice little divider
print("\n**************************************\n")
# Print the last 10 days of data to the screen
os.system("tail -n 10 covidData.txt")
