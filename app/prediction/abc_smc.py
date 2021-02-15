from data_model.Treatment import Treatment
import functools
from scipy.integrate import odeint
import pandas
import numpy as np
import json
import pyabc
import datetime
from itertools import tee
from typing import List, Tuple
from data_model.Measurement import Measurement
from util import unzip

from prediction.util import (
    transform_measurements,
    transform_predictions,
    date_to_offset,
)


def tumor_model(params):
    KDE = params["KDE"]
    lambda_p = params["lambda_p"]
    K = params["K"]
    k_qpp = params["k_qpp"]
    k_pq = params["k_pq"]
    y_p = params["y_p"]
    y_q = params["y_q"]
    delta_qp = params["delta_qp"]

    def f(state, t):
        C, P, Q, Qp = state
        MTD = P + Q + Qp
        dC = -KDE * C
        dP = lambda_p * P * (1 - MTD / K) + k_qpp * Qp - k_pq * P - y_p * C * KDE * P
        dQ = k_pq * P - y_q * C * KDE * Q
        dQp = y_q * C * KDE * Q - k_qpp * Qp - delta_qp * Qp
        return dC, dP, dQ, dQp

    return f


def tumor_ode_solver(
    params, frequency=0.1, time_range=(-10.0, 40.0), treatments=[0], final=False
):
    t_start, t_end = time_range
    model = tumor_model(params)

    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    def t_space(s, e):
        return np.linspace(s, e, num=1 + int(round((e - s) / frequency)))

    t_first_interval_end = treatments[0] if treatments else t_end

    x0 = np.array([0, params["P0"], params["Q0"], 0])
    t = t_space(t_start, t_first_interval_end)
    y = odeint(model, x0, t)
    if final:
        print("y", len(y))

    for t0, t1 in pairwise([*treatments, t_end]):
        P0, Q0, Qp0 = y[-1, 1:]
        C0 = 1
        y = y[:-1]  # delete first element to not be duplicated
        t = t_space(t0, t1)

        x0 = np.array([C0, P0, Q0, Qp0])

        n_y = odeint(model, x0, t)
        y = np.concatenate([y, n_y])
        if final:
            print("y", len(y))

    mtd = y[:, 1] + y[:, 2] + y[:, 3]
    t = t_space(t_start, t_end)

    d = {"t": t, "mtd": mtd, "C": y[:, 0], "P": y[:, 1], "Q": y[:, 2], "Qp": y[:, 3]}
    return pandas.DataFrame(data=d)


# model for pyabc
def abc_model(prediction_time_range, train_time_range, frequency, treatments):
    def f(parameters):
        df = tumor_ode_solver(
            params=parameters,
            frequency=frequency,
            time_range=prediction_time_range,
            treatments=treatments,
        )
        data = df[(df["t"] >= train_time_range[0]) & (df["t"] <= train_time_range[1])]
        return {"data": data["mtd"]}

    return f


def abs_distance(x1, x2):
    return np.sum(np.absolute(x1["data"] - x2["data"]))


def prior(n_percent):
    with open("settings_siwik.config") as config_file:
        config = json.load(config_file)

    def paramRV(range):
        return pyabc.RV("uniform", range[0], range[1])

    def dist(val, n):
        inter_half = 0.01 * n * val
        return val - inter_half / 2, inter_half

    dist_n_percent = functools.partial(dist, n=n_percent)

    return pyabc.Distribution(
        lambda_p=paramRV(dist_n_percent(config["equation_params"]["lambda_p"])),
        K=paramRV(dist_n_percent(config["equation_params"]["K"])),
        k_qpp=paramRV(dist_n_percent(config["equation_params"]["k_qpp"])),
        k_pq=paramRV(dist_n_percent(config["equation_params"]["k_pq"])),
        y_p=paramRV(dist_n_percent(config["equation_params"]["y_p"])),
        y_q=paramRV(dist_n_percent(config["equation_params"]["y_q"])),
        delta_qp=paramRV(dist_n_percent(config["equation_params"]["delta_qp"])),
        KDE=paramRV(dist_n_percent(config["equation_params"]["KDE"])),
        Q0=paramRV(dist_n_percent(config["initial_state"]["Q0"])),
        P0=paramRV(dist_n_percent(config["initial_state"]["P0"])),
    )


def train_patient(
    pat_df,
    training_time_range,
    prediction_time_range,
    treatments=[],
    frequency=0.1,
    n_percent=10,
    epsilon=1,
    populations=20,
):
    train_start, train_end = training_time_range

    train_df = pat_df[(pat_df["t"] >= train_start) & (pat_df["t"] <= train_end)]
    print(len(train_df))

    abc = pyabc.ABCSMC(
        abc_model(prediction_time_range, training_time_range, frequency, treatments),
        prior(n_percent),
        abs_distance,
    )
    db_path = "sqlite:///test.db"

    abc.new(db_path, {"data": train_df["mtd"]})

    history = abc.run(minimum_epsilon=epsilon, max_nr_populations=populations)

    df, w = history.get_distribution()
    best_ind = np.where(w == np.amax(w))
    best_params = df.iloc[best_ind].squeeze()

    return best_params, history


def generate_prediction_abc_smc(
    measurements: List[Measurement],
    prediction_days_number: int,
    treatments: List[Treatment],
) -> List[Tuple[datetime.date, float]]:
    first_date = min(m.date for m in measurements)
    last_date = max(m.date for m in measurements)

    prediction_last_date = last_date + datetime.timedelta(days=prediction_days_number)
    prediction_offset = date_to_offset(first_date, prediction_last_date)
    xs, ys = unzip(transform_measurements(first_date, measurements))

    df = pandas.DataFrame(data={"t": xs, "mtd": ys})

    training_time_range = (0, xs[-1])
    prediction_time_range = (0, prediction_offset)

    transformed_treatments = [date_to_offset(first_date, t.date) for t in treatments]

    train_treatments = [
        t
        for t in transformed_treatments
        if training_time_range[0] <= t <= training_time_range[1]
    ]
    print("train", training_time_range, train_treatments)
    print("predict", prediction_time_range, transformed_treatments)

    params, _ = train_patient(
        df,
        training_time_range,
        prediction_time_range,
        treatments=train_treatments,
        n_percent=50,
        populations=10,
    )
    abc_df = tumor_ode_solver(
        params,
        time_range=prediction_time_range,
        treatments=transformed_treatments,
        final=True,
    )
    return transform_predictions(first_date, [*zip(abc_df["t"], abc_df["mtd"])])
