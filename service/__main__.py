import time
import threading

from db import DB

def execute_job(db, job):
    print('Executing job ' + job)

if __name__ == '__main__':
    db = DB()
    while True:
        for job in db.reserve_pending_jobs():
            print(job)
            threading.Thread(target=execute_job, args=(db,job)).start()
        time.sleep(0.2)
