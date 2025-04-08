import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from db import session, init_db
from models import Job
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PASSWORD = os.getenv("FROM_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

CHROME_BINARY = "/usr/bin/chromium"
CHROMEDRIVER_PATH = "/usr/lib/chromium/chromedriver"

URL = "https://www.glassdoor.com/Job/israel-software-developer-student-or-junior-jobs-SRCH_IL.0,6_IN119_KO7,43.htm"

SELECTORS = {
    "job_card": "JobsList_jobListItem__wjTHv",
    "age": "JobCard_listingAge__jJsuc",
    "company": "EmployerProfile_compactEmployerName__9MGcV",
    "position": "JobCard_jobTitle__GLyJ1",
    "place": "JobCard_location__Ds1fM",
    "link_tag": "a"
}

def create_driver():
    options = Options()
    options.binary_location = CHROME_BINARY
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(FROM_EMAIL, FROM_PASSWORD)
    server.send_message(msg)
    server.quit()

def parse_time_posted(text):
    digits = ''.join([c for c in text if c.isdigit()])
    time_val = int(digits) if digits else 0
    return time_val <= 7 or text.endswith('h')

def extract_job_info(card):
    def get(class_name):
        return card.find_element(By.CLASS_NAME, class_name).text
    def get_link():
        return card.find_element(By.TAG_NAME, SELECTORS["link_tag"]).get_attribute("href")

    return {
        "company": get(SELECTORS["company"]),
        "position": get(SELECTORS["position"]),
        "place": get(SELECTORS["place"]),
        "time_posted": get(SELECTORS["age"]),
        "more_info": get_link()
    }

def process_job(job_data):
    existing = session.query(Job).filter_by(more_info=job_data["more_info"]).first()
    if existing:
        return
    new_job = Job(**job_data)
    session.add(new_job)
    session.commit()
    body = (
        f"Company: {job_data['company']}\n"
        f"Position: {job_data['position']}\n"
        f"Location: {job_data['place']}\n"
        f"Link: {job_data['more_info']}"
    )
    send_email("New Job Alert", body)

def job_scraper():
    init_db()
    driver = create_driver()
    driver.get(URL)
    time.sleep(2)
    job_cards = driver.find_elements(By.CLASS_NAME, SELECTORS["job_card"])
    for card in job_cards:
        try:
            time_text = card.find_element(By.CLASS_NAME, SELECTORS["age"]).text
            if parse_time_posted(time_text):
                job_data = extract_job_info(card)
                process_job(job_data)
        except Exception:
            continue
    driver.quit()
