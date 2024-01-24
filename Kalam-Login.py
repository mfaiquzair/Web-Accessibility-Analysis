#1. Importing needed libraries
import requests
from lxml import html
from bs4 import BeautifulSoup
from csv import writer
from lighthouse import *
import time


#2. Create a session
session_requests = requests.session()


#3. Define URL
login_url = "https://kalam.ump.edu.my/login/index.php"
result = session_requests.get(login_url)


#4. To scrap login token
tree = html.fromstring(result.text)
logintoken= list(set(tree.xpath("//input[@name='logintoken']/@value")))[0]
print(logintoken)

#5. Create payload to login into KALAM
payload = {
    'logintoken' : logintoken,
    'username' : 'null',
    'password' : 'null'
    }

#6. Define POST(to login) and GET(to scrap)
post = session_requests.post(login_url, data=payload)
target = session_requests.get("https://kalam.ump.edu.my/my/") 

#time.sleep(5)

#7. Create a bs object
soup = BeautifulSoup(target.content,'html.parser')
# print(soup.prettify())
link = soup.find("div", "list-group-item list-group-item-action ")
print(link)

# links = soup.find_all('a','aalink')
# 
# for link in links:
#     #href = link.get('href')
#     print(link)
    
# title = soup.find('title')
# print(title)


#8. Find all course links and extract course ID and course link
course_links = soup.select(".aalink") #check balik takut salah
print(course_links)
course_data = []
for link in course_links:
    course_id = link.get("href").split("/")[-2]
    course_link = "https://kalam.ump.edu.my" + link.get("href")
    accessibility_score = run_lighthouse(course_link)
    course_data.append({"course_id": course_id, "course_link": course_link, "accessibility_score": accessibility_score})
    print(f"Course ID: {course_id} | Course Link: {course_link} | Accessibility Score: {accessibility_score}")

#9. Save course data to a CSV file
with open(r"C:\Users\USER\Documents\Python Scripts\course_data.csv", "w", newline="") as csvfile:
    csvwriter = writer(csvfile)
    csvwriter.writerow(["Course ID", "Course Link", "Accessibility Score"])
    for data in course_data:
        csvwriter.writerow([data["course_id"], data["course_link"], data["accessibility_score"]])

