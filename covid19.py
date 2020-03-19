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


def readData():
    """
    Read yesterday's data from the covidData text file.

    This code will grab the last line for daily calculations and deltas.
    """
    with open('covidData.txt', 'r') as fRead:
        for line in fRead:
            pass
        last = line.split(' ')
        yestCaseNum = int(last[10].replace(',', ''))
        yestActive = int(last[16].replace(',', ''))
        yestClosed = int(last[20].replace(',', ''))
        yestRecover = int(last[24].replace(',', ''))
        yestDeaths = int(last[29].replace(',', ''))
        return yestCaseNum, yestActive, yestClosed, yestRecover, yestDeaths


def calDeltas(yCNum, yANum, yClNum, yRNum, yDNum, todayValues):
    """
    Calculate the differences from yesterday's numbers.

    This code will print to the terminal and right now, doesn't write to a
    file.
    """
    # Initialize an array to hold int data
    intVals = []
    for i in range(len(todayValues)):
        # Convert string values to intergers:
        intVals.append(int(todayValues[i].replace(',', '')))
    # Calculate and print case differences
    caseNumDiff = intVals[0] - yCNum
    if intVals[0] > yCNum:
        print(f'The total number of cases increased by {caseNumDiff}'
              f' since yesterday')
    elif caseNumDiff == 0:
        print('Hallelujah, no additional cases!')
    else:
        print(
            f'Hopefully, we have turned the corner. There are '
            f'{abs(caseNumDiff)} less cases today!')
    # Calculate and print active case differences
    caseActiveDiff = intVals[3] - yANum
    if intVals[3] > yANum:
        print(f'Active cases increased by {caseActiveDiff} people')
    elif caseActiveDiff == 0:
        print('Hallelujah, no additional active cases!')
    else:
        print(
            f'Hopefully, we have turned the corner. There are '
            f'{abs(caseActiveDiff)} less active cases today!')
    # Calculate and print death differences
    caseDeathDiff = intVals[1] - yDNum
    if caseDeathDiff > 1:
        print(f'Unfortunately, {caseDeathDiff} people died yesterday')
    elif caseDeathDiff == 1:
        print(f'Unfortunately, {caseDeathDiff} person died yesterday')
    else:
        print('Hallelujah, no additional deaths!')
    # Calculate and print closed case differences
    caseClosedDiff = intVals[4] - yClNum
    if caseClosedDiff > 0:
        print(f'Closed cases increased by {caseClosedDiff}')
    else:
        print('No change in closed cases...')
    # Calculate and print recovered case differences
    caseRecoveredDiff = intVals[2] - yRNum
    if caseRecoveredDiff > 0:
        print(f'{caseRecoveredDiff} people recovered!!!')
    else:
        print('No change in recovered cases...')


def writeData():
    """
    Append the data to covidData.txt.

    Keeps track of daily activity and deltas.
    """
    with open('covidData.txt', 'a') as f:
        f.write(
            f'{today} - Cases today: {values[0]} - Active cases:'
            f' {values[3]} - Closed cases: {values[4]} - Recovered: '
            f'{values[2]} - Deaths: {values[1]}\n')


# Grab the source and keep this assignment under 80 chars
html_source = (requests.get
               ('https://www.worldometers.info/coronavirus/country/us/').text)

# Create the BeautifulSoup object from the source code
soup = BeautifulSoup(html_source, 'lxml')

today = dt.datetime.today().strftime("%m-%d-%Y")

# Print to the terminal after clearing screen
os.system('clear')
print(
    "\n************* United States of America COVID-19 Data ***************\n")
print("Today's date:", today)
# Create 2 empty lists to grab the data from the soup object
labels = []
values = []
# Grab the labels and values from the appropriate divs
for headline in soup.find_all('div', id='maincounter-wrap'):
    labels.append(headline.h1.text.strip(' \n'))
    values.append(headline.find(class_='maincounter-number').text.strip(' \n'))
# Grab the labels and values from the appropriate divs
for cases in soup.find_all('div', class_='col-md-6'):
    labels.append(cases.find(class_='panel-heading').text.strip(' \n'))
    values.append(cases.find(class_='number-table-main').text.strip(' \n'))
# Print to the terminal
for i in range(len(labels)):
    print(labels[i], values[i])
print()
# Read yeseterday's data
yCNum, yANum, yClNum, yRNum, yDNum = readData()

# Caluculate and print the deltas
calDeltas(yCNum, yANum, yClNum, yRNum, yDNum, values)

# Call the function to write today's data
writeData()
# Print a nice little divider
print("\n**************************************\n")
# Print the last 10 days of data to the screen
os.system("tail -n 10 covidData.txt")
