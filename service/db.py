import os
import sqlite3

class DB:

    def __init__(self):
        self.con = sqlite3.connect(os.environ['DB_DIR'] + '/kindlr.db')
