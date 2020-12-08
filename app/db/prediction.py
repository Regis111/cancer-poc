import logging
from datetime import datetime

from data_model.Patient import Patient
from data_model.Prediction import Prediction
from db.config import DATE_FORMAT
from db.util import with_connection, with_connection_and_commit

logging.basicConfig(level=logging.DEBUG)


@with_connection_and_commit
def create_prediction_for_patient(patient, prediction_no, date, value, cursor=None) -> Prediction:
    """Creates a PREDICTION row in db, creates Prediction object and adds it to patient predictions.
    :param patient - Patient class object
    :param prediction_no - chronological number of prediction
    :param date - datetime object
    :param value - float number
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns newly created Prediction object
    """
    cursor.execute(
        "INSERT INTO PREDICTION(PREDICTION_NO, DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?, ?)",
        (prediction_no, date.strftime(DATE_FORMAT), value, patient.db_id),
    )
    prediction_id = cursor.lastrowid
    prediction = Prediction(prediction_id, date, value)
    if patient.predictions[prediction_no]:
        patient.predictions[prediction_no] = [prediction]
    else:
        patient.predictions[prediction_no].append(prediction)
    return prediction


@with_connection_and_commit
def create_predictions_for_patient(patient: Patient, prediction_no: int, dates_values: iter, cursor=None) -> list:
    """Creates a PREDICTION rows in db, creates Prediction object and adds it to patient predictions.
    :param patient - Patient class object
    :param prediction_no - chronological number of prediction
    :param dates_values - iterable of (date, value) tuples
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns list of newly created Prediction objects
    """
    predictions = []
    for date, value in dates_values:
        cursor.execute(
            "INSERT INTO PREDICTION(PREDICTION_NO, DATE, VALUE, PATIENT_ID) VALUES (?, ?, ?, ?)",
            (prediction_no, date.strftime(DATE_FORMAT), value, patient.db_id),
        )
        prediction_id = cursor.lastrowid
        predictions.append(Prediction(prediction_id, date, value))
    patient.predictions[prediction_no] = predictions
    return predictions


@with_connection
def get_predictions_for_patient_id(patient_id: int, cursor=None) -> dict:
    """Fetches predictions from db for a given patient_id."""
    cursor.execute("SELECT * FROM PREDICTION WHERE PATIENT_ID=?", (patient_id,))
    predictions = {}
    for prediction_id, prediction_no, date, value, _ in cursor.fetchall():
        if predictions[prediction_no]:
            predictions[prediction_no].append(Prediction(prediction_id, datetime.strptime(date, DATE_FORMAT), value))
        else:
            predictions[prediction_no] = [Prediction(prediction_id, datetime.strptime(date, DATE_FORMAT), value)]
    return predictions


@with_connection_and_commit
def delete_all_predictions_for_patient(patient: Patient, cursor=None):
    """Deletes all predictions for given patient both in db and object"""
    cursor.executemany(
        "DELETE FROM PREDICTION WHERE ID=?", [(p.db_id,) for p in patient.predictions]
    )
    patient.predictions.clear()
    logging.debug(
        f"Deleted predictions for patient: {patient} with id: {patient.db_id}"
    )
