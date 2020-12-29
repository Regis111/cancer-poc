from db.patient import create_patient, get_all_patients
from db.measurement import (
    create_measurements_for_patient,
    delete_all_measurements_for_patient,
)
from datetime import timedelta, date
import pandas
import argparse
import logging


def import_patient(
    patient: int,
    patient_name: str,
    density: int,
    measurements_stop: int,
):
    logging.debug(
        "Importing patient %s with density equal %d and measurements_stop equal %d",
        patient,
        density,
        measurements_stop,
    )
    initial_date: date = date(2000, 1, 1)
    df = pandas.read_csv(f"resources/abc_pat_{patient}.csv")
    measurements_stop = (
        measurements_stop if measurements_stop != None else df.index.stop
    )
    pat = [
        patient
        for patient in get_all_patients()
        if patient.name == "ribba" and patient.surname == patient_name
    ]
    if len(pat) == 0:
        pat = create_patient("ribba", patient_name)
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
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="import patient from resources/")
    parser.add_argument(
        "--patient",
        "-p",
        action="store",
        choices=[2, 8, 17],
        type=int,
        required=True,
        help="describes which person to import",
    )
    parser.add_argument(
        "--patient_name",
        "-pn",
        action="store",
        type=str,
        required=True,
        help="name of patient",
    )
    parser.add_argument(
        "--density",
        "-d",
        action="store",
        type=int,
        default=1,
        required=False,
        help="describes frequency of imported data eg. density=3 means taking every 3rd value",
    )
    parser.add_argument(
        "--measurements_stop",
        "-ms",
        action="store",
        type=int,
        required=False,
        help="describes how many rows to import",
    )
    args = vars(parser.parse_args())
    import_patient(**args)
