# GetJobs

**GetJobs** is a job scraping service that automatically scrapes new software development job listings from Glassdoor (Israel, student/junior level), stores them in a SQLite database, and sends you an email when new jobs are found.

> Built with Python, Selenium, Flask, SQLAlchemy, and Docker.

---

##  Features

-  Smart scraping with Selenium 
-  Email alerts for new job listings
-  SQLite database to avoid duplicates
-  Scheduled job scraping
-  Dockerized for local or server deployment

---

##  Requirements

- Docker 
- Or: Python 3.10+ and Google Chrome/Chromium installed locally

---



## How to Use

### 1. Clone the Repository

<pre> ```bash git clone https://github.com/Razana3008/getJobs.git cd getJobs ``` </pre>



### 2. Create .env File

Copy the example and fill in your email credentials:
cp .env.example .env
Then edit .env and provide the following:
FROM_EMAIL=your_email@gmail.com
FROM_PASSWORD=your_email_password_or_app_password
TO_EMAIL=recipient_email@example.com
Gmail users: Use an App Password if 2FA is enabled.


### 3. Build and Run with Docker

<pre> ```bash docker build -t getjobs . docker run --env-file .env -p 5000:5000 getjobs ``` </pre>





