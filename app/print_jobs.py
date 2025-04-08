from db import session, init_db
from models import Job

# Ensure the DB and tables are initialized
init_db()

# Query all jobs
jobs = session.query(Job).all()

print(f"\n Found {len(jobs)} job(s):\n")
for job in jobs:
    print(f"{job.company} - {job.position} ({job.place})")
    print(f"Posted: {job.time_posted} | Link: {job.more_info}")
    print("-" * 80)


