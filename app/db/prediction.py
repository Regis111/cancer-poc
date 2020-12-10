import logging
from datetime import datetime, date
from typing import List, Dict, Tuple

from data_model.Patient import Patient
from data_model.PredictionValue import PredictionValue
from db.config import DATE_FORMAT
from db.util import with_connection, with_connection_and_commit

logging.basicConfig(level=logging.DEBUG)


@with_connection_and_commit
def create_prediction_for_patient(
    patient: Patient,
    creation_datetime: datetime,
    dates_values: List[Tuple[date, float]],
    cursor=None,
) -> Dict[datetime, List[PredictionValue]]:
    """Creates a PREDICTION rows in db, creates PredictionValue object and adds it to patient predictions.
    :param patient - Patient class object
    :param creation_datetime - prediction creation datetime
    :param dates_values - iterable of (date, value) tuples
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns dictionary of newly created "predictions"
    """
    cursor.execute(
        "INSERT INTO PREDICTION(DATETIME_CREATED, PATIENT_ID) VALUES (?, ?)",
        (creation_datetime.isoformat(), patient.db_id),
    )
    prediction_id = cursor.lastrowid
    predictions = []
    for value_date, value in dates_values:
        cursor.execute(
            "INSERT INTO PREDICTION_VALUE(DATE, VALUE, PREDICTION_ID) VALUES (?, ?, ?)",
            (value_date.strftime(DATE_FORMAT), value, prediction_id),
        )
        prediction_value_id = cursor.lastrowid
        predictions.append(PredictionValue(prediction_value_id, value_date, value))
    patient.predictions[creation_datetime] = predictions
    return patient.predictions


@with_connection
def get_predictions_for_patient_id(patient_id: int, cursor=None) -> dict:
    """Fetches predictions from db for a given patient_id."""
    cursor.execute(
        """SELECT P.DATETIME_CREATED, PV.ID, PV.DATE, PV.VALUE
        FROM PREDICTION P
        JOIN PREDICTION_VALUE PV on P.ID = PV.PREDICTION_ID
        WHERE P.PATIENT_ID=?""",
        (patient_id,),
    )
    predictions = {}
    for creation_datetime, prediction_value_id, value_date, value in cursor.fetchall():
        prediction = PredictionValue(
            prediction_value_id,
            datetime.strptime(value_date, DATE_FORMAT).date(),
            value,
        )
        creation_datetime = datetime.fromisoformat(creation_datetime)
        if creation_datetime in predictions:
            predictions[creation_datetime].append(prediction)
        else:
            predictions[creation_datetime] = [prediction]
    return predictions


@with_connection_and_commit
def delete_prediction_for_patient(
    patient: Patient, creation_datetime: datetime, cursor=None
) -> Patient:
    cursor.execute(
        "DELETE FROM PREDICTION WHERE PATIENT_ID=? AND DATETIME_CREATED=?",
        (patient.db_id, creation_datetime.isoformat()),
    )
    patient.predictions.pop(creation_datetime)
    logging.debug(
        f"Deleted prediction created at {creation_datetime} for patient: {patient}"
    )


@with_connection_and_commit
def delete_all_predictions_for_patient(patient: Patient, cursor=None):
    """Deletes all predictions for given patient both in db and object"""
    cursor.execute("DELETE FROM PREDICTION WHERE PATIENT_ID=?", (patient.db_id,))
    patient.predictions.clear()
    logging.debug(
        f"Deleted predictions for patient: {patient} with id: {patient.db_id}"
    )
