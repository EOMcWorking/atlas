import sqlite3


DB_FILE = "atlas.db"


def get_connection():

    return sqlite3.connect(
        DB_FILE
    )