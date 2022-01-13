import os
import sqlite3

from job import Job

class DB:

    def __init__(self):
        self.con = self.open_connection()
        cur = self.con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id              TEXT PRIMARY KEY,
                file            TEXT NOT NULL,
                skip_conversion INTEGER TEXT NOT NULL,
                step            TEXT,
                state           TEXT,
                message         TEXT,
                time            TEXT
            );
        ''')

    def reserve_pending_jobs(self):
        cur = self.con.cursor()
        rows = cur.execute('SELECT id, file, skip_conversion FROM jobs WHERE step IS NULL ORDER BY time').fetchall()
        cur.execute("UPDATE jobs SET step = 'reserved' WHERE step IS NULL")
        self.con.commit()
        return map(lambda r: Job(r[0], r[1], r[2]), rows)

    def set_step(self, job, step, state, message=None):
        con = self.open_connection()
        cur = con.cursor()
        cur.execute('''
            UPDATE jobs
               SET step = ?
                 , state = ?
                 , message = ?
             WHERE id = ?''', (step, state, message, job))
        con.commit()
        con.close()

    def open_connection(self):
        return sqlite3.connect(os.environ['DB_DIR'] + '/kindlr.db', check_same_thread=False)
