import logging
from datetime import date, datetime
from typing import List, Tuple

from data_model.Measurement import Measurement
from data_model.Patient import Patient
from db.config import DATE_FORMAT
from db.util import with_connection, with_connection_and_commit


@with_connection_and_commit
def create_measurement_for_patient(
    patient: Patient, measurement_date: date, value: float, cursor=None
) -> Measurement:
    """Creates a MEASUREMENT row in db, creates Measurement object and adds it to patient measurements.
    :param patient - Patient class object
    :param measurement_date - datetime object
    :param value - float number
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns newly created Measurement object
    """
    cursor.execute(
        "INSERT INTO MEASUREMENT(DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?)",
        (measurement_date.strftime(DATE_FORMAT), value, patient.db_id),
    )
    logging.debug(
        "Inserted measurement %s, %s",
        measurement_date,
        value,
    )
    measurement_id = cursor.lastrowid
    measurement = Measurement(measurement_id, measurement_date, value)
    patient.measurements.append(measurement)
    return measurement


@with_connection_and_commit
def create_measurements_for_patient(
    patient: Patient, dates_values: List[Tuple[date, float]], cursor=None
) -> List[Measurement]:
    """Creates a MEASUREMENT rows in db, creates Measurement object and adds it to patient measurements.
    :param patient - Patient class object
    :param dates_values - iterable of (date, value) tuples
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns list of newly created Measurement objects
    """
    measurements = []
    for measurement_date, value in dates_values:
        cursor.execute(
            "INSERT INTO MEASUREMENT(DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?)",
            (measurement_date.strftime(DATE_FORMAT), value, patient.db_id),
        )
        logging.debug(
            "Inserted measurement %s, %s",
            measurement_date,
            value,
        )
        measurement_id = cursor.lastrowid
        measurements.append(Measurement(measurement_id, measurement_date, value))
    patient.measurements += measurements
    return measurements


@with_connection
def get_measurements_for_patient_id(patient_id: int, cursor=None) -> List[Measurement]:
    """Fetches measurements from db for a given patient_id."""
    cursor.execute("SELECT * FROM MEASUREMENT WHERE PATIENT_ID=?", (patient_id,))
    return [
        Measurement(
            measurement_id,
            datetime.strptime(measurement_date, DATE_FORMAT).date(),
            value,
        )
        for measurement_id, measurement_date, value, _ in cursor.fetchall()
    ]


@with_connection_and_commit
def delete_measurement_for_patient(
    patient: Patient, measurement: Measurement, cursor=None
):
    """Deletes measurement for given patient both in db and object"""
    cursor.execute("DELETE FROM MEASUREMENT WHERE ID=?", (measurement.db_id,))
    patient.measurements.remove(measurement)


@with_connection_and_commit
def delete_all_measurements_for_patient(patient: Patient, cursor=None):
    """Deletes all measurements for given patient both in db and object"""
    cursor.executemany(
        "DELETE FROM MEASUREMENT WHERE ID=?", [(m.db_id,) for m in patient.measurements]
    )
    logging.debug(
        "Removed all measurements of patient %s",
        patient,
    )
    patient.measurements.clear()
