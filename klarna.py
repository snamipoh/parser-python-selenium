from selenium import webdriver
from datetime import date
import time
import sqlite3


chromedriver = "C:\\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
driver.get("https://jobs.lever.co/klarna")

# Accept cookie
driver.find_element_by_xpath("//div[@class='cc-compliance']").click()
time.sleep(5)

jobs = []

titles = driver.find_elements_by_xpath("//*[@class='posting-title']/h5")
links = driver.find_elements_by_xpath("//*[@class='posting-title']")
locations = driver.find_elements_by_xpath("//*[@class='posting-title']//span[@class='sort-by-location posting-category small-category-label']")
job_type = "Other"
job_company = "klarna"
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
    if "analyst" in element['title'].lower() or "data scientist" in element['title'].lower() \
            or "business intelligence developer" in element['title'].lower() \
            or "data" in element['title'].lower() or "etl developer" in element['title'].lower():
        element['job_type'] = "Data & BI"
    elif "designer" in element['title'].lower() or "product design" in element['title'].lower() \
            or "product designer" in element['title'].lower() or "ux writer" in element['title'].lower():
        element['job_type'] = "Design"
    elif "product manager" in element['title'].lower():
        element['job_type'] = "Product"
    elif "security" in element['title'].lower():
        element['job_type'] = "Security"
    elif "devops" in element['title'].lower():
        element['job_type'] = "DevOps"
    elif "Script" in element['title'] or "react" in element['title'].lower() \
            or "vue" in element['title'].lower() or "front" in element['title'].lower():
        element['job_type'] = "Frontend"
    elif "Java" in element['title']:
        element['job_type'] = "Java"
    elif "sre" in element['title'].lower() or "site reliability engineer" in element['title'].lower():
        element['job_type'] = "SRE"
    elif "python" in element['title'].lower() or "site reliability engineer" in element['title'].lower():
        element['job_type'] = "Backend"
    elif "php" in element['title'].lower() or "site reliability engineer" in element['title'].lower():
        element['job_type'] = "Backend"
    elif "android" in element['title'].lower() or "site reliability engineer" in element['title'].lower():
        element['job_type'] = "Android"
    elif "ios" in element['title'].lower() or "site reliability engineer" in element['title'].lower():
        element['job_type'] = "iOS"
    else:
        element['job_type'] = "Other"


for element in jobs:
    if "amsterdam" in element['location'].lower():
        element['location'] = "Netherlands"
    elif "berlin" in element['location'].lower():
        element['location'] = "Germany"
    elif "giessen" in element['location'].lower():
        element['location'] = "Germany"
    elif "madrid" in element['location'].lower():
        element['location'] = "Spain"
    elif "munich" in element['location'].lower():
        element['location'] = "Germany"
    elif "stockholm" in element['location'].lower():
        element['location'] = "Sweden"
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
