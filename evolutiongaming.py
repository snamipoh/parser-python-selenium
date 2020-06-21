from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import date
import sqlite3


chromedriver = "C:\\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.evolutiongamingcareers.com/search-jobs/?department=&country=")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

while True:
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='more-jobs-button']"))).click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except TimeoutException:
        break

jobs = []

titles = driver.find_elements_by_xpath("//*[@id='listOfJobs']//div[@class='nectar-list-item titleColor']")
links = driver.find_elements_by_xpath("//*[@id='listOfJobs']//a[@href]")
locations = driver.find_elements_by_xpath("//*[@id='listOfJobs']//div[@data-text-align='right']")
job_type = "Other"
job_company = "evolution gaming"
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

# Deleting unnecessary words after parsing locations
for job in jobs:
    index_number = job["location"].find(" ")
    # print(index_number)
    job["location"] = job["location"][index_number + 1:]

job_type_position = (
    (["javascript", "typescript", "react", "angular", "vue", "front"], "Frontend"),
    (["scala"], "Scala"),
    (["devops"], "DevOps"),
    (["product owner"], "Product"),
    (["qa"], "QA"),
    (["data analyst", "database developer", "data center engineer", "big data", "analyst", "data scientist", "bi analyst", "data engineer", "business intelligence", "business analyst"], "Data & BI"),
    (["sre", "site reliability engineer"], "SRE"),
    (["security", "security engineer"], "Security"),
    (["groovy", "groovy engineer"], "Groovy"),
    (["embedded software developer", "embedded software engineer", "embedded"], "Embedded SW"),
    (["ux/ui designer", "ux researcher", "designer", "ux designer"], "Design"),
    (["backend", "back"], "Backend")
)

map_country = {
    "netherlands": "Netherlands",
    "malta": "Malta",
    "romania": "Romania",
    "belarus": "Belarus",
    "latvia": "Latvia",
    "belgium": "Belgium",
    "estonia": "Estonia"
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
