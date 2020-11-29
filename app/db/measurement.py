from datetime import datetime

from data_model.Measurement import Measurement
from db.config import DATE_FORMAT
from db.util import with_connection, with_connection_and_commit
import logging

logging.basicConfig(level=logging.DEBUG)


@with_connection_and_commit
def create_measurement_for_patient(patient, date, value, cursor=None):
    """Creates a MEASUREMENT row in db, creates Measurement object and adds it to patient measurements.
    :param patient - Patient class object
    :param date - datetime object
    :param value - float number
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns newly created Measurement object
    """
    cursor.execute(
        "INSERT INTO MEASUREMENT(DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?)",
        (date.strftime(DATE_FORMAT), value, patient.db_id),
    )
    measurement_id = cursor.lastrowid
    measurement = Measurement(measurement_id, date, value)
    patient.measurements.append(measurement)
    return measurement


@with_connection_and_commit
def create_measurements_for_patient(patient, dates_values, cursor=None):
    """Creates a MEASUREMENT rows in db, creates Measurement object and adds it to patient measurements.
    :param patient - Patient class object
    :param dates_values - iterable of (date, value) tuples
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns list of newly created Measurement objects
    """
    measurements = []
    for date, value in dates_values:
        cursor.execute(
            "INSERT INTO MEASUREMENT(DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?)",
            (date.strftime(DATE_FORMAT), value, patient.db_id),
        )
        logging.debug("Inserted measurement %s, %s", date, value)
        measurement_id = cursor.lastrowid
        measurements.append(Measurement(measurement_id, date, value))
    patient.measurements += measurements
    return measurements


@with_connection
def get_measurements_for_patient_id(patient_id, cursor=None):
    """Fetches measurements from db for a given patient_id."""
    cursor.execute("SELECT * FROM MEASUREMENT WHERE PATIENT_ID=?", (patient_id,))
    return [
        Measurement(measurement_id, datetime.strptime(date, DATE_FORMAT), value)
        for measurement_id, date, value, _ in cursor.fetchall()
    ]


@with_connection_and_commit
def delete_measurement_for_patient(patient, measurement, cursor=None):
    """Deletes measurement for given patient both in db and object"""
    cursor.execute("DELETE FROM MEASUREMENT WHERE ID=?", (measurement.db_id,))
    patient.measurements.remove(measurement)


@with_connection_and_commit
def delete_all_measurements_for_patient(patient, cursor=None):
    """Deletes all measurements for given patient both in db and object"""
    cursor.executemany(
        "DELETE FROM MEASUREMENT WHERE ID=?", [(m.db_id,) for m in patient.measurements]
    )
    patient.measurements.clear()
