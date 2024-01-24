from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from csv import writer
from lighthouse import *
driver = webdriver.Chrome('./chromedriver')


#Go to the login URL
driver.get("https://kalam.ump.edu.my/login/index.php")


## Search for the input field and input the username and password
username = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
username.send_keys("null")
password.send_keys("null")

#Search for the login button and click it
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()



#Wait for 3 seconds
time.sleep(5)
print("Now let start copying the data from the website")


#Select all the courses
listOfCourses = driver.find_elements(By.CSS_SELECTOR,  "div[role='listitem']")

course_data = []


#Loop through the list of course and sand the info for each courses
for singleCourse in listOfCourses:
    course_link = singleCourse.find_element(By.TAG_NAME, "a").get_attribute("href")
    course_id = course_link.split("id=")[-1]
    accessibility_score = run_lighthouse(course_link)
    course_data.append({"course_id": course_id, "course_link": course_link, "accessibility_score": accessibility_score})
    print(f"Course ID: {course_id} | Course Link: {course_link} | Accessibility Score: {accessibility_score}")

#Save course data to a CSV file
with open(r"course_data.csv", "w", newline="") as csvfile:
    csvwriter = writer(csvfile)
    csvwriter.writerow(["Course ID", "Course Link", "Accessibility Score"])
    for data in course_data:
        csvwriter.writerow([data["course_id"], data["course_link"], data["accessibility_score"]])



#Leave the web driver
driver.quit()
