from db.initialize import init
from db.measurement import *
from db.patient import *
from db.prediction import *

if __name__ == '__main__':
    # example usage of db module
    init()
    patient = create_patient('Elton', 'John')
    print(patient.db_id)
    create_measurements_for_patient(patient, [(datetime(2020, 8, 10), 21.6), (datetime(2020, 8, 20), 22.6)])
    create_predictions_for_patient(patient, [(datetime(2020, 8, 30), 25.1), (datetime(2020, 9, 9), 28.9)])
    create_measurement_for_patient(patient, datetime(2020, 8, 30), 24.7)
    delete_all_predictions_for_patient(patient)
    create_predictions_for_patient(patient, [(datetime(2020, 9, 9), 27.4), (datetime(2020, 9, 19), 28.1)])

    patients = get_all_patients()
    for patient in patients:
        print(patient.db_id, patient.name, patient.surname, patient.measurements, patient.predictions)
        delete_patient(patient)
        # after this db should be empty
