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
driver.get("https://n26.com/en/careers/locations/57663")


# Accept cookie

while True:
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept all']"))).click()
    except TimeoutException:
        break

jobs = []

# Parsing vacancies from Barcelona
section = driver.find_elements_by_xpath("//ul[@class='ah aj al an ap aq jp kd ke kf kg']//li")

for i in section:

    jobs.append({
        'title': i.find_element_by_css_selector("a").get_property("text"),
        'link': i.find_element_by_css_selector("a").get_attribute("href"),
        'location': "Spain",
        'job_type': "Other",
        'job_company': "n26",
        'job_date': str(date.today())
    })

# print(jobs)

# Parsing vacancies from Berlin
# driver.execute_script("window.scrollTo(0, 400)")
driver.find_element_by_xpath("//a[@href='/en/careers/locations/49747']").click()
time.sleep(10)

section_2 = driver.find_elements_by_xpath("//ul[@class='ah aj al an ap aq jp kd ke kf kg']//li")
time.sleep(5)

for i in section_2:

    jobs.append({
        'title': i.find_element_by_css_selector("a").get_property("text"),
        'link': i.find_element_by_css_selector("a").get_attribute("href"),
        'location': "Germany",
        'job_type': "Other",
        'job_company': "n26",
        'job_date': str(date.today())
    })

# print(jobs)

# Deleting unnecessary words and symbols after parsing vacancy titles
for job in jobs:
    index_number = job["title"].find("Location")
    # print(index_number)
    job["title"] = job["title"][:index_number]

# print(jobs)

for job in jobs:
    if "security" in job['title'].lower() or "security engineer" in job['title'].lower():
        job['job_type'] = "Security"
    elif "tech lead" in job['title'].lower() or "engineering manager" in job['title'].lower() \
            or "head of infrastructure" in job['title'].lower() \
            or "director of technology" in job['title'].lower() \
            or "head of engineering" in job['title'].lower():
        job['job_type'] = 'Tech Lead'
    elif "data analyst" in job['title'].lower() or "big data" in job['title'].lower() \
            or "analyst" in job['title'].lower() or "data scientist" in job['title'].lower() \
            or "bi analyst" in job['title'].lower() or "data engineer" in job['title'].lower() \
            or "business intelligence" in job['title'].lower() or "machine learning" in job['title'].lower():
        job['job_type'] = 'Data & BI'
    elif "sre" in job['title'].lower() or "site reliability engineer" in job['title'].lower():
        job['job_type'] = 'SRE'
    elif "devops" in job['title'].lower():
        job['job_type'] = "DevOps"
    elif "director of product design" in job['title'].lower() or "UX researcher" in job['title'].lower() \
            or "designer" in job['title'].lower() or "ux designer" in job['title'].lower():
        job['job_type'] = "Design"
    elif "backend" in job['title'].lower() or "back" in job['title'].lower():
        job['job_type'] = "Backend"
    elif "javascript" in job['title'].lower() or "typescript" in job['title'].lower() \
            or "react" in job['title'].lower() or "angular" in job['title'].lower() \
            or "vue" in job['title'].lower() or "front" in job['title'].lower():
        job['job_type'] = "Frontend"
    else:
        job['job_type'] = "Other"

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
