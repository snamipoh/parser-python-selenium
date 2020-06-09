from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import date
import sqlite3


chromedriver = "C:\\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.smartly.io/careers")

# Accept cookie
while True:
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']"))).click()
    except TimeoutException:
        break

# Download all vacancies
driver.find_element_by_xpath("//div[@class='b-listing-open-positions__listing__show-all js-b-listing-open-positions--unminimize']").click()

jobs = []

titles = driver.find_elements_by_xpath("//div[@class='c-open-position']//div[@class='c-open-position__title']")
links = driver.find_elements_by_xpath("//div[@class='c-open-position']//a[@class='c-open-position__overlay-link']")
locations = driver.find_elements_by_xpath("//div[@class='c-open-position']//div[@class='c-open-position__meta__item']")
job_type = "Other"
job_company = "smartly.io"
job_date = str(date.today())

num_values = len(titles)

for i in range(num_values):

    jobs.append({
        'title': titles[i].text,
        'link': links[i].get_attribute("href"),
        'location': locations[i].text,
        'job_type': job_type,
        'job_company': job_company,
        'job_date': job_date
    })

# print(jobs)

for element in jobs:
    if "devops" in element['title'].lower():
        element['job_type'] = "DevOps"
    elif "product designer" in element['title'].lower():
        element['job_type'] = "Design"
    elif "backend developer" in element['title'].lower() or "back" in element['title'].lower() \
            or "backend/fullstack" in element['title'].lower():
        element['job_type'] = "Backend"
    elif "javascript" in element['title'].lower() or "typescript" in element['title'].lower() \
            or "react" in element['title'].lower() or "angular" in element['title'].lower() \
            or "vue" in element['title'].lower() or "front" in element['title'].lower():
        element['job_type'] = "Frontend"
    elif "fullstack" in element['title'].lower() or "full stack" in element['title'].lower() \
            or "full-stack" in element['title'].lower():
        element['job_type'] = "Fullstack"
    else:
        element['job_type'] = "Other"

for element in jobs:
    if "helsinki" in element['location'].lower():
        element['location'] = "Finland"
    else:
        element['location'] = "Other"

# print(jobs)

# Converting dict into list of tuples
tuples = [tuple(x.values())[0:] for x in jobs]
print(tuples)

# Uncomment to upload parsed records to the DB

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.executemany("INSERT INTO jobs (job_title, job_link, job_location, job_type, job_company, job_date) VALUES(?, "
                   "?, ?, ?, ?, ?)", tuples) 

conn.commit()
conn.close()


driver.quit()
