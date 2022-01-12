import os
import sqlite3

class DB:

    def __init__(self):
        self.con = sqlite3.connect(os.environ['DB_DIR'] + '/kindlr.db')
        self.con.cursor().execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id              TEXT PRIMARY KEY,
                file            TEXT NOT NULL,
                skip_conversion INTEGER TEXT NOT NULL,
                step            TEXT,
                state           TEXT,
                message         TEXT
            );
        ''')

    def set_step(self, job, step, state, message=None):
        cur = self.con.cursor()
        cur.begin()
        cur.execute('''
            UPDATE jobs
               SET step = ?
                 , state = ?
                 , message = ?
             WHERE id = ?''', (step, state, job, message))
        cur.commit()
        cur.close()
