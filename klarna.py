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

# Deleting unnecessary words after parsing locations
for job in jobs:
    index_number = job["location"].find(",")
    # print(index_number)
    job["location"] = job["location"][:index_number]

job_type_position = (
    (["devops"], "DevOps"),
    (["analyst", "data analyst", "bi analyst", "data engineer", "data scientist", "business intelligence", "data warehouse"], "Data & BI"),
    (["product manager", "product marketing"], "Product"),
    (["designer", "product design", "product designer", "ux writer", "ux research"], "Design"),
    (["backend", "back", "python", "php"], "Backend"),
    (["javascript", "typescript", "react", "angular", "vue", "front"], "Frontend"),
    (["fullstack", "full stack", "full-stack"], "Fullstack"),
    (["security"], "Security"),
    (["android"], "Android"),
    (["ios"], "iOS"),
    (["java", "senior backend engineer - java"], "Java"),
    (["sre", "site reliability engineer"], "SRE")
)

map_country = {
    "amsterdam": "Netherlands",
    "berlin": "Germany",
    "munich": "Germany",
    "giessen": "Germany",
    "madrid": "Spain",
    "stockholm": "Sweden"
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
