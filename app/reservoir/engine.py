import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from esn.esn import DeepESN, DeepSubreservoirESN
from esn import activation as activ
from esn.initialization import *
from scipy.integrate import odeint
import torch
from typing import List, Tuple
from data_model.Measurement import Measurement
from data_model.Prediction import Prediction
from scipy.interpolate import make_interp_spline

np.random.seed(42)

device = torch.device('cpu')
dtype = torch.double
torch.set_default_dtype(dtype)


def create_prediction(measurements: List[Measurement]) -> List[tuple]:
    transformed_measurements = _transform_measurements(measurements)
    x, y = _interpolate_missing_days(transformed_measurements)
    return _predict(x, y)


def _transform_measurements(measurements: List[Measurement]) -> List[tuple]:
    first_date = min(m.date for m in measurements)

    def date_to_offset(date):
        return (date - first_date).days

    return sorted((date_to_offset(m.date), m.value) for m in measurements)


def _interpolate_missing_days(measurements: List[tuple]) -> Tuple[np.ndarray, np.ndarray]:
    x, y = _unzip(measurements)
    spline_degree = len(x) - 1 if len(x) < 4 else 3
    spline_fun = make_interp_spline(x, y, k=spline_degree)
    dense_x = np.array(list(range(x[0], x[-1] + 1)))
    dense_y = spline_fun(dense_x)
    return dense_x, dense_y


def _unzip(iterable):
    return list(zip(*iterable))


def _to_tensor(array: np.ndarray) -> Tensor:
    reshaped = array.reshape((-1, 1, 1))
    return torch.from_numpy(reshaped).to(device)


def _predict(x: np.ndarray, y: np.ndarray) -> List[tuple]:
    x_pred = list(range(x[-1] + 1, x[-1] + len(x)))
    x, y = _to_tensor(y[:-1]), _to_tensor(y[1:])
    esn = DeepESN(1, 100, initializer=WeightInitializer(), num_layers=3, bias=False,
                  activation=activ.relu(leaky_rate=0.5), transient=len(x) // 2)
    esn.fit(x, y)
    y_pred = []
    p = y[-1:]
    n = len(x_pred)
    for i in range(n):
        p = esn(p)
        p = torch.reshape(p, (1, 1, 1))
        y_pred.append(p.item())
    return list(zip(x_pred, y_pred))


def test():
    measurements_ = [
        Measurement(2, datetime.datetime(2020, 11, 25), 15),
        Measurement(1, datetime.datetime(2020, 11, 20), 10),
        Measurement(3, datetime.datetime(2020, 11, 30), 17)
    ]
    print(create_prediction(measurements_))
