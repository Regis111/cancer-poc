import csv
import json
import numpy as np
from scipy.integrate import odeint


def cancer(equation_params):
    K = equation_params["K"]
    lambda_p = equation_params["lambda_p"]
    k_pq = equation_params["k_pq"]
    k_qpp = equation_params["k_qpp"]
    delta_qp = equation_params["delta_qp"]
    y = equation_params["y"]
    KDE = equation_params["KDE"]

    def f(state, t):
        C, P, Q, Qp = state
        MTD = P + Q + Qp
        dC = -KDE * C
        dP = lambda_p * P * (1 - MTD / K) + k_qpp * Qp - k_pq * P - y * C * KDE * P
        dQ = k_pq * P - y * C * KDE * Q
        dQp = y * C * KDE * Q - k_qpp * Qp - delta_qp * Qp
        return dC, dP, dQ, dQp

    return f


config_file_name = "settings.config"

with open(config_file_name) as config_file:
    config = json.load(config_file)
    C0 = config["initial_state"]["C0"]
    P0 = config["initial_state"]["P0"]
    Q0 = config["initial_state"]["Q0"]
    Qp0 = config["initial_state"]["Qp0"]

    x0 = np.array([C0, P0, Q0, Qp0])
    t = np.arange(0.0, 30.0, 0.1)

    equations = cancer(config["equation_params"])

    states_0 = odeint(equations, x0, t)
    MTD_0 = states_0[:, 1] + states_0[:, 2] + states_0[:, 3]

    C0 = 1
    P0 = states_0[-1, 1]
    Q0 = states_0[-1, 2]
    Qp0 = states_0[-1, 3]

    x0 = np.array([C0, P0, Q0, Qp0])
    t = np.arange(30.0, 60.0, 0.1)

    states_1 = odeint(equations, x0, t)
    MTD_1 = states_1[:, 1] + states_1[:, 2] + states_1[:, 3]

    states = np.concatenate((states_0, states_1), axis=0)
    MTD = np.concatenate((MTD_0, MTD_1), axis=0)

    with open("data.csv", mode="w") as csv_file:
        fieldnames = ["P0", "Q0", "Qp0", "MTD"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i, state in enumerate(states):
            entry = {"P0": state[1], "Q0": state[2], "Qp0": state[3], "MTD": MTD[i]}
            writer.writerow(entry)
