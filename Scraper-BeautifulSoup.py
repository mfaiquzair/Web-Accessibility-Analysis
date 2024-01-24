import requests
from bs4 import BeautifulSoup

# Define the URL of the page to scrape 
url = 'https://www.ump.edu.my/en'

# Send a GET request to the URL and store the response
response = requests.get(url)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <a> tags in the parsed HTML content
links = soup.find_all('a')

# Loop through each <a> tag and print the value of the href attribute
for link in links:
    print(link.get('href'))

# Repeat the above steps for the second page
url = 'https://www.ump.edu.my/en?page=1'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')
for link in links:
    print(link.get('href'))
    



