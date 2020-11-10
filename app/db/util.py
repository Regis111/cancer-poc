import sqlite3

from db.config import DB_PATH


def with_connection_and_commit(function):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_PATH)
        kwargs['cursor'] = conn.cursor()
        result = function(*args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return wrapper


def with_connection(function):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_PATH)
        kwargs['cursor'] = conn.cursor()
        result = function(*args, **kwargs)
        conn.close()
        return result

    return wrapper
