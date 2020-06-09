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

# Scrolling down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Click element to download vacancies
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

for element in jobs:
    if "javascript" in element['title'].lower() or "typescript" in element['title'].lower() \
            or "react" in element['title'].lower() or "angular" in element['title'].lower() \
            or "vue" in element['title'].lower() or "front" in element['title'].lower():
        element['job_type'] = "Frontend"
    elif "scala" in element['title'].lower():
        element['job_type'] = "Scala"
    elif "devops" in element['title'].lower():
        element['job_type'] = "DevOps"
    elif "product owner" in element['title'].lower():
        element['job_type'] = "Product"
    elif "qa" in element['title'].lower():
        element['job_type'] = "QA"
    elif "data analyst" in element['title'].lower() or "database developer" in element['title'].lower() \
            or "data center engineer" in element['title'].lower() or "big data" in element['title'].lower() \
            or "analyst" in element['title'].lower() or "data scientist" in element['title'].lower() \
            or "bi analyst" in element['title'].lower() or "data engineer" in element['title'].lower() \
            or "business intelligence" in element['title'].lower() or "business analyst" in element['title'].lower():
        element['job_type'] = "Data & BI"
    elif "sre" in element['title'].lower() or "site reliability engineer" in element['title'].lower():
        element['job_type'] = 'SRE'
    elif "security" in element['title'].lower() or "security engineer" in element['title'].lower():
        element['job_type'] = 'Security'
    elif "groovy" in element['title'].lower() or "groovy engineer" in element['title'].lower():
        element['job_type'] = "Groovy"
    elif "embedded software developer" in element['title'].lower() \
            or "embedded software engineer" in element['title'].lower() or "embedded" in element['title'].lower():
        element['job_type'] = "Embedded SW"
    elif "ux/ui designer" in element['title'].lower() or "UX researcher" in element['title'].lower() \
            or "designer" in element['title'].lower() or "ux designer" in element['title'].lower():
        element['job_type'] = 'Designer'
    elif "backend" in element['title'].lower() or "back" in element['title'].lower():
        element['job_type'] = "Backend"
    else:
        element['job_type'] = "Other"

for element in jobs:
    if "netherlands" in element['location'].lower():
        element['location'] = "Netherlands"
    elif "malta" in element['location'].lower():
        element['location'] = "Malta"
    elif "romania" in element['location'].lower():
        element['location'] = "Romania"
    elif "belarus" in element['location'].lower():
        element['location'] = "Belarus"
    elif "latvia" in element['location'].lower():
        element['location'] = "Latvia"
    elif "belgium" in element['location'].lower():
        element['location'] = "Belgium"
    elif "estonia" in element['location'].lower():
        element['location'] = "Estonia"
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
