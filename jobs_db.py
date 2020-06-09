import sqlite3

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

c.execute("""CREATE TABLE jobs (
        job_title text,
        job_link text,
        job_location text,
        job_type text,
        job_company text,
        job_date text
    )""")

conn.commit()

conn.close()
