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
# locations = driver.find_elements_by_xpath("//div[@class='c-open-position']//div[@class='c-open-position__meta__item']/span")
locations = driver.find_elements_by_xpath("//div[@class='c-open-position']//span[@data-position-location]")
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

job_type_position = (
    (["devops"], "DevOps"),
    (["data"], "Data & BI"),
    (["product manager", "product marketing"], "Product"),
    (["designer"], "Design"),
    (["backend", "back", "backend/fullstack"], "Backend"),
    (["frontend", "front", "javascript", "typescript"], "Frontend"),
    (["fullstack", "full stack", "full-stack"], "Fullstack"),
    (["security", "security engineer"], 'Security'),
    (["groovy", "groovy engineer"], "Groovy"),
    (["embedded software developer", "embedded software engineer", "embedded"], "Embedded SW"),
    (["ux/ui designer", "ux researcher", "designer", "ux designer"], 'Design')
)

map_country = {
    "helsinki": "Finland"
}


def get_job_type(title):
    for job_titles, job_type in job_type_position:
        for job_title in job_titles:
            if job_title in title:
                return job_type
    return 'Other'


for element in jobs:
    title = element['title'].lower()
    job_type = get_job_type(title)
    element['job_type'] = job_type

    location = element['location'].lower()
    location_clean = map_country.get(location, 'Other')
    element['location'] = location_clean

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
