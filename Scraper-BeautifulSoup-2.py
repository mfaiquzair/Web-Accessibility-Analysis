import requests
import csv
from bs4 import BeautifulSoup

# Define the URL of the page to scrape
url1 = 'https://www.ump.edu.my/en'
url2 = 'https://www.ump.edu.my/en?page=1'

# Send a GET request to the URL and store the response
response1 = requests.get(url1)
response2 = requests.get(url2)

# Parse the HTML content of the response using BeautifulSoup
soup1 = BeautifulSoup(response1.content, 'html.parser')
soup2 = BeautifulSoup(response2.content, 'html.parser')

# Find all <a> tags in the parsed HTML content
links1 = soup1.find_all('a')
links2 = soup2.find_all('a')

# Define a list to store the links
all_links = []

# Loop through each <a> tag and append the value of the href attribute to the list
for link in links1:
    all_links.append(link.get('href'))

for link in links2:
    all_links.append(link.get('href'))

# Define the name of the CSV file to save the data to
filename = "ump_links.csv"

# Open the CSV file in write mode and write the links to it
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Link"])

    for link in all_links:
        writer.writerow([link])

