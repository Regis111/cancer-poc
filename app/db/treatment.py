import logging
from typing import List
from datetime import date, datetime
from data_model.Patient import Patient
from db.util import with_connection, with_connection_and_commit
from data_model.Treatment import Treatment
from db.config import DATE_FORMAT


@with_connection
def get_treatments_for_patient_id(patient_id: int, cursor=None) -> List[Treatment]:
    cursor.execute("SELECT * FROM TREATMENT WHERE PATIENT_ID=?", (patient_id,))
    return [
        Treatment(
            treatment_id,
            datetime.strptime(treatment_date, DATE_FORMAT).date(),
            treatment_amount,
        )
        for treatment_id, treatment_date, treatment_amount, _ in cursor.fetchall()
    ]


@with_connection_and_commit
def create_treatment_for_patient(
    patient: Patient, treatment_date: date, amount: int, cursor=None
) -> Treatment:
    cursor.execute(
        "INSERT INTO TREATMENT(DATE, AMOUNT, PATIENT_ID) VALUES (?, ?, ?)",
        (treatment_date.strftime(DATE_FORMAT), amount, patient.db_id),
    )
    logging.debug(
        "Inserted measurement %s",
        treatment_date,
    )
    treatment_id = cursor.lastrowid
    treatment = Treatment(treatment_id, treatment_date, amount)
    patient.treatments.append(treatment)
    return treatment


@with_connection_and_commit
def delete_treatment_for_patient(patient: Patient, treatment: Treatment, cursor=None):
    cursor.execute(
        "DELETE FROM TREATMENT WHERE ID=?",
        (treatment.db_id,),
    )
    logging.debug("Deleted treatment %s of %s", treatment.date, patient)
    patient.treatments.remove(treatment)
