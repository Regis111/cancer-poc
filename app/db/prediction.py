import logging
from datetime import datetime, date
from typing import List, Tuple

from data_model.Patient import Patient
from data_model.Prediction import Prediction
from data_model.PredictionValue import PredictionValue
from db.config import DATE_FORMAT, DATETIME_FORMAT
from db.util import with_connection, with_connection_and_commit


@with_connection_and_commit
def create_prediction_for_patient(
    patient: Patient,
    method: str,
    creation_datetime: datetime,
    dates_values: List[Tuple[date, float]],
    cursor=None,
) -> Prediction:
    """Creates a PREDICTION rows in db, creates PredictionValue object and adds it to patient predictions.
    :param patient - Patient class object
    :param method - prediction method name
    :param creation_datetime - prediction creation datetime
    :param dates_values - iterable of (date, value) tuples
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns dictionary of newly created "predictions"
    """
    cursor.execute(
        "INSERT INTO PREDICTION(DATETIME_CREATED, METHOD, PATIENT_ID) VALUES (?, ?, ?)",
        (creation_datetime.strftime(DATETIME_FORMAT), method, patient.db_id),
    )
    logging.debug(
        "Inserted Prediction %s, %s, %s",
        creation_datetime.strftime(DATETIME_FORMAT),
        method,
        patient.db_id,
    )
    prediction_id = cursor.lastrowid
    prediction_values: List[PredictionValue] = []
    for value_date, value in dates_values:
        cursor.execute(
            "INSERT INTO PREDICTION_VALUE(DATE, VALUE, PREDICTION_ID) VALUES (?, ?, ?)",
            (value_date.strftime(DATE_FORMAT), value, prediction_id),
        )
        logging.debug(
            "Inserted PredictionValue %s, %s, %s",
            value_date.strftime(DATE_FORMAT),
            value,
            prediction_id,
        )
        prediction_value_id = cursor.lastrowid
        prediction_values.append(
            PredictionValue(prediction_value_id, value_date, value)
        )
    prediction = Prediction(
        prediction_id, prediction_values, creation_datetime, method, patient.db_id
    )
    patient.predictions.append(prediction)
    return prediction


@with_connection
def get_predictions_for_patient_id(patient_id: int, cursor=None) -> List[Prediction]:
    """Fetches predictions from db for a given patient_id."""
    cursor.execute(
        "SELECT P.ID, P.DATETIME_CREATED, P.METHOD FROM PREDICTION P WHERE P.PATIENT_ID=?",
        (patient_id,),
    )
    predictions = [
        Prediction(
            prediction_id,
            [],
            datetime.strptime(creation_datetime, DATETIME_FORMAT),
            prediction_method,
            patient_id,
        )
        for prediction_id, creation_datetime, prediction_method in cursor.fetchall()
    ]
    for p in predictions:
        cursor.execute(
            "SELECT PV.ID, PV.DATE, PV.VALUE FROM PREDICTION_VALUE PV WHERE PV.PREDICTION_ID=?",
            (p.db_id,),
        )
        p.prediction_values = [
            PredictionValue(
                pv_id, datetime.strptime(pv_date, DATE_FORMAT).date(), pv_value
            )
            for pv_id, pv_date, pv_value in cursor.fetchall()
        ]
    return predictions


@with_connection_and_commit
def delete_prediction_for_patient(
    patient: Patient, creation_datetime: datetime, cursor=None
) -> Patient:
    cursor.execute(
        "DELETE FROM PREDICTION WHERE PATIENT_ID=? AND DATETIME_CREATED=?",
        (patient.db_id, creation_datetime.strftime(DATETIME_FORMAT)),
    )
    patient.predictions = get_predictions_for_patient_id(patient.db_id)
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
