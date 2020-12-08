import datetime
from typing import Tuple

import numpy as np
import torch
from esn import activation
from esn.esn import DeepESN
from esn.initialization import *
from scipy.interpolate import make_interp_spline

from data_model.Measurement import Measurement
from util import unzip

np.random.seed(42)

device = torch.device("cpu")
dtype = torch.double
torch.set_default_dtype(dtype)


def generate_prediction(measurements: List[Measurement]) -> List[Tuple]:
    """Creates prediction for given measurements.
    Time range of generated predictions is the same as time range of measurements,
    i.e. it starts the day after the last measurement and lasts for the same number of days as
    the difference between first and last measurement.
    :returns list of tuples (date, value)"""
    first_date = min(m.date for m in measurements)
    transformed_measurements = _transform_measurements(first_date, measurements)
    x, y = _interpolate_missing_days(transformed_measurements)
    predictions = _predict(x, y)
    return _transform_predictions(first_date, predictions)


def _transform_measurements(first_date: datetime.date, measurements: List[Measurement]) -> List[tuple]:
    def date_to_offset(date):
        return (date - first_date).days

    return sorted((date_to_offset(m.date), m.value) for m in measurements)


def _interpolate_missing_days(measurements: List[tuple]) -> Tuple[np.ndarray, np.ndarray]:
    x, y = unzip(measurements)
    spline_degree = len(x) - 1 if len(x) < 4 else 3
    spline_fun = make_interp_spline(x, y, k=spline_degree)
    dense_x = np.array(list(range(x[0], x[-1] + 1)))
    dense_y = spline_fun(dense_x)
    dense_y = dense_y.astype(float)
    return dense_x, dense_y


def _to_tensor(array: np.ndarray) -> Tensor:
    reshaped = array.reshape((-1, 1, 1))
    return torch.from_numpy(reshaped).to(device)


def _predict(day_offsets: np.ndarray, values: np.ndarray) -> List[tuple]:
    day_offsets_pred = list(
        range(day_offsets[-1] + 1, day_offsets[-1] + len(day_offsets))
    )
    x, y = _to_tensor(values[:-1]), _to_tensor(values[1:])
    esn = DeepESN(
        1,
        100,
        initializer=WeightInitializer(),
        num_layers=3,
        bias=False,
        activation=activation.relu(leaky_rate=0.5),
        transient=len(day_offsets) // 2,
    )
    esn.fit(x, y)
    y_pred = []
    p = torch.from_numpy(values[-1:])
    p = torch.reshape(p, (1, 1, 1))
    n = len(day_offsets_pred)
    for _ in range(n):
        p = esn(p)
        p = torch.reshape(p, (1, 1, 1))
        y_pred.append(p.item())
    return list(zip(day_offsets_pred, y_pred))


def _transform_predictions(first_date: datetime.date, predictions: List[tuple]):
    def offset_to_date(day_offset):
        return first_date + datetime.timedelta(days=day_offset)

    return [(offset_to_date(off), val) for off, val in predictions]


def test():
    measurements = [
        Measurement(1, datetime.date(2020, 11, 20), 10),
        Measurement(2, datetime.date(2020, 11, 25), 15),
        Measurement(3, datetime.date(2020, 11, 30), 17),
        Measurement(3, datetime.date(2020, 12, 2), 19),
    ]
    print(generate_prediction(measurements))


if __name__ == "__main__":
    test()
