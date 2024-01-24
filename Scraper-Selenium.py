from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
# from lighthouse import LighthouseRunner
import time
from csv import writer

# initialize web driver and service 
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)

# navigate to the login page
driver.get("https://kalam.ump.edu.my/login/index.php")

# input username and password and click login button
username = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
username.send_keys("null")
password.send_keys("null")
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

# wait for 5 seconds to allow page loading
time.sleep(5)
print("Now let's start copying the data from the website")

# get all the course links
listOfCourses = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
course_data = []

# function to run lighthouse for a given url
def run_lighthouse(url):
    runner = Runner(url)
    report = runner.run()
    score = report['categories']['accessibility']['score'] * 100
    return score

# loop through the list of courses and get info for each course
for singleCourse in listOfCourses:
    course_link = singleCourse.find_element(By.TAG_NAME, "a").get_attribute("href")
    course_id = course_link.split("id=")[-1]
    accessibility_score = run_lighthouse(course_link)
    course_data.append({"course_id": course_id, "course_link": course_link, "accessibility_score": accessibility_score})
    print(f"Course ID: {course_id} | Course Link: {course_link} | Accessibility Score: {accessibility_score}")

# save course data to a CSV file
with open(r"course_data.csv", "w", newline="") as csvfile:
    csvwriter = writer(csvfile)
    csvwriter.writerow(["Course ID", "Course Link", "Accessibility Score"])
    for data in course_data:
        csvwriter.writerow([data["course_id"], data["course_link"], data["accessibility_score"]])

# quit the web driver
driver.quit()

