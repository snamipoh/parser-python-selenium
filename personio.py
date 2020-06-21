from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import date
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
        'title': i.find_element_by_css_selector("p.h3").text,
        'link': i.find_element_by_css_selector("a.personio_yellow_button_medium").get_attribute("href"),
        'location': i.find_element_by_css_selector("p.w-10").text,
        'job_type': "Other",
        'job_company': "personio",
        'job_date': str(date.today())
    })

# print(jobs)

job_type_position = (
    (["devops"], "DevOps"),
    (["data analyst", "bi analyst", "data engineer", "business intelligence"], "Data & BI"),
    (["product manager", "product marketing"], "Product"),
    (["designer"], "Design"),
    (["backend", "back"], "Backend"),
    (["frontend", "front", "javascript", "typescript"], "Frontend"),
    (["fullstack", "full stack", "full-stack"], "Fullstack"),
    (["security", "security engineer"], "Security"),
    (["ux/ui designer", "ux researcher", "designer", "ux designer"], "Design"),
    (["engineering manager", "head of infrastructure", "director of technology", "director of product"], "Tech Lead")
)

map_country = {
    "munich": "Germany",
    "madrid": "Spain"
}


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
