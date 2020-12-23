from db.patient import create_patient, get_all_patients
from db.measurement import (
    create_measurements_for_patient,
    delete_all_measurements_for_patient,
)
from datetime import timedelta, date
import pandas


def import_patient(
    patient_no: str,
    patient_no_name: str,
    initial_date: date = date(2000, 1, 1),
    density: int = 1,
    measurements_stop: int = -1,
):
    df = pandas.read_csv(f"resources/abc_pat_{patient_no}.csv")
    measurements_stop = measurements_stop if measurements_stop != -1 else df.index.stop
    pat = [
        patient
        for patient in get_all_patients()
        if patient.name == "ribba" and patient.surname == patient_no_name
    ]
    if len(pat) == 0:
        pat = create_patient("ribba", patient_no_name)
    else:
        pat = pat[0]
        delete_all_measurements_for_patient(pat)

    dates = [
        initial_date + timedelta(days=n) for n in range(0, measurements_stop, density)
    ]
    values = df["mtd"][0:measurements_stop:density]
    dates_values = list(zip(dates, values))
    create_measurements_for_patient(pat, dates_values)


if __name__ == "__main__":
    # import_patient("2", "second", density=5)
    # import_patient("8", "eighth")
    import_patient("17", "seventeen", density=5)