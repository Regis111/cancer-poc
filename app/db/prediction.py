import logging
from datetime import date, datetime

from data_model.Patient import Patient
from data_model.Prediction import Prediction
from db.config import DATE_FORMAT
from db.util import with_connection, with_connection_and_commit

logging.basicConfig(level=logging.DEBUG)


@with_connection_and_commit
def create_prediction_for_patient(
    patient: Patient, creation_date: date, dates_values: iter, cursor=None
) -> dict:
    """Creates a PREDICTION rows in db, creates Prediction object and adds it to patient predictions.
    :param patient - Patient class object
    :param creation_date - prediction creation date
    :param dates_values - iterable of (date, value) tuples
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns list of newly created Prediction objects
    """
    cursor.execute(
        "INSERT INTO PREDICTION(DATE_CREATED, PATIENT_ID) VALUES (?, ?)",
        (creation_date.strftime(DATE_FORMAT), patient.db_id),
    )
    prediction_id = cursor.lastrowid
    predictions = []
    for value_date, value in dates_values:
        cursor.execute(
            "INSERT INTO PREDICTION_VALUE(DATE, VALUE, PREDICTION_ID) VALUES (?, ?, ?)",
            (value_date.strftime(DATE_FORMAT), value, prediction_id),
        )
        prediction_value_id = cursor.lastrowid
        predictions.append(Prediction(prediction_value_id, value_date, value))
    patient.predictions[creation_date] = predictions
    return patient.predictions


@with_connection
def get_predictions_for_patient_id(patient_id: int, cursor=None) -> dict:
    """Fetches predictions from db for a given patient_id."""
    cursor.execute(
        """SELECT P.DATE_CREATED, PV.ID, PV.DATE, PV.VALUE
        FROM PREDICTION P
        JOIN PREDICTION_VALUE PV on P.ID = PV.PREDICTION_ID
        WHERE P.PATIENT_ID=?""",
        (patient_id,),
    )
    predictions = {}
    for creation_date, prediction_value_id, value_date, value in cursor.fetchall():
        prediction = Prediction(
            prediction_value_id,
            datetime.strptime(value_date, DATE_FORMAT).date(),
            value,
        )
        if creation_date in predictions:
            predictions[creation_date].append(prediction)
        else:
            predictions[creation_date] = [prediction]
    return predictions


@with_connection_and_commit
def delete_all_predictions_for_patient(patient: Patient, cursor=None):
    """Deletes all predictions for given patient both in db and object"""
    cursor.execute(
        "SELECT P.ID FROM PREDICTION P WHERE P.PATIENT_ID=?", (patient.db_id,)
    )
    prediction_ids = cursor.fetchall()
    cursor.executemany(
        "DELETE FROM PREDICTION_VALUE WHERE PREDICTION_ID=?",
        [(id,) for id in prediction_ids],
    )
    cursor.execute("DELETE FROM PREDICTION WHERE PATIENT_ID=?", (patient.db_id,))
    patient.predictions.clear()
    logging.debug(
        f"Deleted predictions for patient: {patient} with id: {patient.db_id}"
    )
