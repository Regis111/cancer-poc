import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
from db.patient import create_patient
from db.measurement import create_measurements_for_patient
from db.treatment import create_treatment_for_patient
from datetime import date
import argparse
import json
from prediction.abc_smc import tumor_ode_solver
from typing import Sequence
from prediction.util import offset_to_date


def import_patient(
    patient_name: str, length: int, frequency: float, treatments: Sequence[int]
):
    def generate_patient(config, frequency, time_range, treatments):
        params = config["equation_params"]
        params["P0"] = config["initial_state"]["P0"]
        params["Q0"] = config["initial_state"]["Q0"]

        return tumor_ode_solver(
            params, frequency=frequency, time_range=time_range, treatments=treatments
        )

    logging.debug(
        "Importing patient with datset length %d and treatments at %s",
        length,
        treatments,
    )
    with open("settings_siwik.config") as config:
        config = json.load(config)

    df = generate_patient(
        config, frequency=frequency, time_range=(0, length), treatments=treatments
    )

    pat = create_patient("ribba", patient_name)

    first_date = date(2000, 1, 1)
    print(df["t"])
    dates = [offset_to_date(first_date, t) for t in df["t"]]
    # print(dates)
    values = df["mtd"]
    dates_values = list(zip(dates, values))
    # print(dates_values)
    create_measurements_for_patient(pat, dates_values)

    treatment_dates = [offset_to_date(first_date, tr) for tr in treatments]
    for td in treatment_dates:
        create_treatment_for_patient(pat, td, 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="import ribba patient")
    parser.add_argument(
        "--patient_name",
        "-pn",
        action="store",
        type=str,
        required=True,
        help="name of patient",
    )
    parser.add_argument(
        "--treatments",
        "-t",
        action="store",
        nargs="+",
        type=int,
        required=False,
        default=[],
        help="name of patient",
    )
    parser.add_argument(
        "--length",
        "-l",
        action="store",
        type=int,
        default=50,
        required=False,
        help="length of generated dataset",
    )
    parser.add_argument(
        "--frequency",
        "-f",
        action="store",
        type=float,
        default=0.1,
        required=False,
        help="frequency of generated dataset",
    )
    args = vars(parser.parse_args())
    print(args)
    import_patient(**args)
