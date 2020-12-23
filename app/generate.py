from scipy.integrate import odeint
import pandas
import numpy as np


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


def single_tumor_ode_solver(state, params, time_range, treatment_timepoint=0):
    start, end = time_range
    timepoints_before = np.arange(start, treatment_timepoint, 0.1)
    timepoints_after = np.arange(treatment_timepoint, end, 0.1)

    model = tumor_model(params)

    x0 = state
    y_0 = odeint(model, x0, timepoints_before)

    C0 = 1
    P0 = y_0[-1, 1]
    Q0 = y_0[-1, 2]
    Qp0 = y_0[-1, 3]
    x0 = np.array([C0, P0, Q0, Qp0])

    y_1 = odeint(model, x0, timepoints_after)
    y_1 = y_1[1:]  # delete first element to not be duplicated

    y = np.concatenate((y_0, y_1))

    timepoints_after = timepoints_after[1:]
    timepoints = np.concatenate((timepoints_before, timepoints_after))

    MTD = y[:, 1] + y[:, 2] + y[:, 3]

    pd = pandas.DataFrame(data=y, columns=["C", "P", "Q", "Qp"])
    pd.insert(0, "mtd", MTD)
    pd.insert(0, "t", timepoints)
    return pd


def generate_patient(config, time_range):
    C0 = 0
    P0 = config["P0"].iloc[0]
    Q0 = config["Q0"].iloc[0]
    Qp0 = 0

    abc_state = np.array([C0, P0, Q0, Qp0])

    abc_params = config[
        ["K", "KDE", "delta_qp", "k_pq", "k_qpp", "lambda_p", "y_p", "y_q"]
    ].to_dict(orient="list")

    for key, val in abc_params.items():
        abc_params[key] = val[0]

    return single_tumor_ode_solver(abc_state, abc_params, time_range)


if __name__ == "__main__":
    pat2 = pandas.read_csv("resources/pat_id_2.csv").sort_values(by=["t"])
    pat8 = pandas.read_csv("resources/pat_id_8.csv").sort_values(by=["t"])
    pat17 = pandas.read_csv("resources/pat_id_17.csv").sort_values(by=["t"])

    params_2 = pandas.read_csv("resources/params2.csv")
    params_8 = pandas.read_csv("resources/params8.csv")
    params_17 = pandas.read_csv("resources/params17.csv")

    time_range_2 = pat2["t"].iloc[0], pat2["t"].iloc[-1]
    time_range_8 = pat8["t"].iloc[0], pat8["t"].iloc[-1]
    time_range_17 = pat17["t"].iloc[0], pat17["t"].iloc[-1]

    pd = generate_patient(params_2, time_range_2)
    pd.to_csv("resources/abc_pat_2.csv")

    pd = generate_patient(params_8, time_range_8)
    pd.to_csv("resouces/abc_pat_8.csv")

    pd = generate_patient(params_17, time_range_17)
    pd.to_csv("resources/abc_pat_17.csv")
