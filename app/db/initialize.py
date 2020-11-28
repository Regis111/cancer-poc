import sqlite3

import db.config as config


def init():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS PATIENT
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME           TEXT   NOT NULL,
                    SURNAME        TEXT   NOT NULL);"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS MEASUREMENT
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    DATE           TEXT   NOT NULL,
                    VALUE          REAL   NOT NULL,
                    PATIENT_ID     INT    NOT NULL,
                    FOREIGN KEY(PATIENT_ID) REFERENCES PATIENT(ID));"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS PREDICTION
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    DATE           TEXT   NOT NULL,
                    VALUE          REAL   NOT NULL,
                    PATIENT_ID     INT    NOT NULL,
                    FOREIGN KEY(PATIENT_ID) REFERENCES PATIENT(ID));"""
    )
    conn.close()
    print("DB initialized successfully")
