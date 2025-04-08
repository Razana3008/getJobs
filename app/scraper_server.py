import threading
import time
import schedule
from flask import Flask, render_template_string
from db import session, init_db
from models import Job
from jobScraper import job_scraper

#  Initialize the database once on startup
init_db()

# === Scraper Thread ===

def run_scraper_schedule():
    schedule.every(50).seconds.do(job_scraper)
    while True:
        schedule.run_pending()
        time.sleep(1)

scraper_thread = threading.Thread(target=run_scraper_schedule, daemon=True)
scraper_thread.start()

# === Flask App ===

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GetJobs</title>
    <style>
        body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
        .job { background: #fff; padding: 15px; margin-bottom: 10px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .title { font-weight: bold; }
        .meta { color: #777; }
        a { color: #0077cc; text-decoration: none; }
    </style>
</head>
<body>
    <h1>GetJobs – Latest Listings</h1>
    {% for job in jobs %}
    <div class="job">
        <div class="title">{{ job.position }}</div>
        <div class="meta">{{ job.company }} – {{ job.place }}</div>
        <div class="meta">Posted: {{ job.time_posted }}</div>
        <a href="{{ job.more_info }}" target="_blank">View</a>
    </div>
    {% else %}
    <p>No jobs available.</p>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    jobs = session.query(Job).order_by(Job.created_at.desc()).all()
    return render_template_string(HTML_TEMPLATE, jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
