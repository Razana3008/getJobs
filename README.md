# GetJobs

**GetJobs** is a job scraping service that automatically scrapes new software development job listings from Glassdoor (Israel, student/junior level), stores them in a SQLite database, and sends you an email when new jobs are found.

> Built with Python, Selenium, Flask, SQLAlchemy, and Docker.

---

##  Features

-  Smart scraping with Selenium (undetected-chromedriver)
-  Email alerts for new job listings
-  SQLite database to avoid duplicates
-  Scheduled job scraping
-  Dockerized for local or server deployment

---

##  Requirements

- Docker 
- Or: Python 3.10+ and Google Chrome/Chromium installed locally

---

##  Run with Docker

### 1. Clone the repo:
```bash
git clone https://github.com/your-username/getJobs.git
cd getJobs
