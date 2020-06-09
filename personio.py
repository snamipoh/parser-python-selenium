from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import date
import time
import sqlite3


chromedriver = "C:\\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.personio.com/about-personio/jobs/")

# Accept cookie
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='hs-eu-confirmation-button']"))).click()

# Download all vacancies
while True:
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='job-board']/a[1]"))).click()
    except TimeoutException:
        break

jobs = []

section = driver.find_elements_by_xpath("//div[@id='job-board']//div")

for i in section:

    jobs.append({
        'job_title': i.find_element_by_css_selector("p.h3").text,
        'job_link': i.find_element_by_css_selector("a.personio_yellow_button_medium").get_attribute("href"),
        'job_location': i.find_element_by_css_selector("p.w-10").text,
        'job_type': "Other",
        'job_company': "personio",
        'job_date': str(date.today())
    })

    for element in jobs:
        if "frontend" in element['job_title'].lower() or "front" in element['job_title'].lower():
            element['job_type'] = "Frontend"
        elif "backend" in element['job_title'].lower() or "back" in element['job_title'].lower():
            element['job_type'] = "Backend"
        elif "data analyst" in element['job_title'].lower() or "bi analyst" in element['job_title'].lower() \
                or "data engineer" in element['job_title'].lower() \
                or "business intelligence" in element['job_title'].lower():
            element['job_type'] = "Data & BI"
        elif "engineering manager" in element['job_title'].lower() \
                or "head of infrastructure" in element['job_title'].lower() \
                or "director of technology" in element['job_title'].lower() \
                or "director of product" in element['job_title'].lower():
            element['job_type'] = "Tech Lead"
        else:
            element['job_type'] = "Other"

for element in jobs:
    if "munich" in element['job_location'].lower():
        element['job_location'] = "Germany"
    elif "madrid" in element['job_location'].lower():
        element['job_location'] = "Spain"
    else:
        element['job_location'] = "Other"

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
