import requests
from lxml import html
from bs4 import BeautifulSoup
from csv import writer
from lighthouse import *


class KalamScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session_requests = requests.session()

    def scrape(self):
        login_url = "https://kalam.ump.edu.my/login/index.php"
        result = self.session_requests.get(login_url)
        tree = html.fromstring(result.text)
        logintoken = list(set(tree.xpath("//input[@name='logintoken']/@value")))[0]

        payload = {
            'logintoken': logintoken,
            'username': self.username,
            'password': self.password
        }
        self.session_requests.post(login_url, data=payload)
        target = self.session_requests.get("https://kalam.ump.edu.my/my/")
        soup = BeautifulSoup(target.content, 'html.parser')

        course_links = soup.select(".aalink")
        course_data = []

        for link in course_links:
            course_id = link.get("href").split("/")[-2]
            course_link = "https://kalam.ump.edu.my" + link.get("href")
            accessibility_score = run_lighthouse(course_link)
            course_data.append({"course_id": course_id, "course_link": course_link, "accessibility_score": accessibility_score})
            print(f"Course ID: {course_id} | Course Link: {course_link} | Accessibility Score: {accessibility_score}")

        with open("course_data.csv", "w", newline="") as csvfile:
            csvwriter = writer(csvfile)
            csvwriter.writerow(["Course ID", "Course Link", "Accessibility Score"])
            for data in course_data:
                csvwriter.writerow([data["course_id"], data["course_link"], data["accessibility_score"]])


scraper = KalamScraper(username='null', password='null')
scraper.scrape()

