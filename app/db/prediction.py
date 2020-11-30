from datetime import datetime

from data_model.Prediction import Prediction
from db.config import DATE_FORMAT
from db.util import with_connection, with_connection_and_commit
import logging

logging.basicConfig(level=logging.DEBUG)


@with_connection_and_commit
def create_prediction_for_patient(patient, date, value, cursor=None):
    """Creates a PREDICTION row in db, creates Prediction object and adds it to patient predictions.
    :param patient - Patient class object
    :param date - datetime object
    :param value - float number
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns newly created Prediction object
    """
    cursor.execute(
        "INSERT INTO PREDICTION(DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?)",
        (date.strftime(DATE_FORMAT), value, patient.db_id),
    )
    prediction_id = cursor.lastrowid
    prediction = Prediction(prediction_id, date, value)
    patient.predictions.append(prediction)
    return prediction


@with_connection_and_commit
def create_predictions_for_patient(patient, dates_values, cursor=None):
    """Creates a PREDICTION rows in db, creates Prediction object and adds it to patient predictions.
    :param patient - Patient class object
    :param dates_values - iterable of (date, value) tuples
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns list of newly created Prediction objects
    """
    predictions = []
    for date, value in dates_values:
        cursor.execute(
            "INSERT INTO PREDICTION(DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?)",
            (date.strftime(DATE_FORMAT), value, patient.db_id),
        )
        prediction_id = cursor.lastrowid
        predictions.append(Prediction(prediction_id, date, value))
    patient.predictions += predictions
    return predictions


@with_connection
def get_predictions_for_patient_id(patient_id, cursor=None):
    """Fetches predictions from db for a given patient_id."""
    cursor.execute("SELECT * FROM PREDICTION WHERE PATIENT_ID=?", (patient_id,))
    return [
        Prediction(prediction_id, datetime.strptime(date, DATE_FORMAT), value)
        for prediction_id, date, value, _ in cursor.fetchall()
    ]


@with_connection_and_commit
def delete_prediction_for_patient(patient, prediction, cursor=None):
    """Deletes prediction for given patient both in db and object"""
    cursor.execute("DELETE FROM PREDICTION WHERE ID=?", (prediction.db_id,))
    patient.predictions.remove(prediction)


@with_connection_and_commit
def delete_all_predictions_for_patient(patient, cursor=None):
    """Deletes all predictions for given patient both in db and object"""
    cursor.executemany(
        "DELETE FROM PREDICTION WHERE ID=?", [(m.db_id,) for m in patient.predictions]
    )
    patient.predictions.clear()
    logging.debug(f"Deleted predictions for patient: {patient} with id: {patient.db_id}")
