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
# driver.find_element_by_xpath("//a[@href='/en/careers/locations/49747']").click()
driver.find_element_by_xpath("//li[@class='cn co cp du jp jq jr']/a[@href='/en/careers/locations/49747']").click()
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

job_type_position = (
    (["data analyst", "big data", "analyst", "data scientist", "bi analyst", "data engineer", "business intelligence", "machine learning"], "Data & BI"),
    (["director of product design", "UX researcher", "designer", "ux designer"], "Design"),
    (["backend", "back"], "Backend"),
    (["frontend", "front", "javascript", "typescript"], "Frontend"),
    (["security", "security engineer"], "Security"),
    (["tech lead", "engineering manager", "head of infrastructure", "director of technology", "head of engineering"], "Tech Lead"),
    (["site reliability engineer"], "SRE"),
    (["devops"], "DevOps")
)


def get_job_type(title):
    for job_titles, job_type in job_type_position:
        for job_title in job_titles:
            if job_title in title:
                return job_type
    return "Other"


for element in jobs:
    title = element['title'].lower()
    job_type = get_job_type(title)
    element['job_type'] = job_type


# print(jobs)

# Converting dict into list of tuples
tuples = [tuple(x.values())[0:] for x in jobs]
print(tuples)
print(len(tuples))

# Uploading parsed records to the DB

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.executemany("INSERT INTO jobs (job_title, job_link, job_location, job_type, job_company, job_date) VALUES(?, "
                   "?, ?, ?, ?, ?)", tuples) 

conn.commit()
conn.close()


driver.quit()
