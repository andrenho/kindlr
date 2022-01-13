import time
import threading

from db import DB
from job import Job

if __name__ == '__main__':
    db = DB()
    while True:
        for job in db.reserve_pending_jobs():
            threading.Thread(target=Job.execute_job, args=(job,db)).start()
        time.sleep(0.2)
