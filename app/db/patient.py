import db.measurement
import db.prediction
from data_model.Patient import Patient
from db.util import with_connection, with_connection_and_commit


@with_connection
def get_all_patients(cursor=None):
    """Fetches all patients from db"""
    patients = []
    cursor.execute('SELECT * FROM PATIENT')
    for patient_id, name, surname in cursor.fetchall():
        measurements = db.measurement.get_measurements_for_patient_id(patient_id)
        predictions = db.prediction.get_predictions_for_patient_id(patient_id)
        patient = Patient(patient_id, name, surname, measurements, predictions)
        patients.append(patient)
    return patients


@with_connection_and_commit
def create_patient(name, surname, cursor=None):
    """Creates a PATIENT row in db and creates Patient object.
    :param name - patient name
    :param surname - patient surname
    :param cursor - cursor provided by with_connection_and_commit decorator
    :returns newly created Patient object
    """
    cursor.execute('INSERT INTO PATIENT(NAME, SURNAME) VALUES (?, ?)',
                   (name, surname))
    patient_id = cursor.lastrowid
    return Patient(patient_id, name, surname, [], [])


@with_connection_and_commit
def delete_patient(patient, cursor=None):
    """Deletes patient from db along with its measurements and predictions."""
    db.measurement.delete_all_measurements_for_patient(patient)
    db.prediction.delete_all_predictions_for_patient(patient)
    cursor.execute('DELETE FROM PATIENT WHERE ID=?',
                   (patient.db_id,))