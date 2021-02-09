import datetime
from datetime import date
from typing import Tuple, List

import numpy as np
import torch
from esn import activation
from esn.esn import DeepESN, DeepSubreservoirESN, SVDReadout, DeepESNCell, ESNBase

from esn.initialization import WeightInitializer, SubreservoirWeightInitializer
from scipy.interpolate import make_interp_spline
from torch import Tensor
from data_model.Measurement import Measurement
from util import unzip

np.random.seed(42)

device = torch.device("cpu")
dtype = torch.double
torch.set_default_dtype(dtype)

AUGMENTATION_CONST = 10
AUGMENTATION_DENSITY = 1 / AUGMENTATION_CONST


def generate_prediction_deep_esn(
    measurements: List[Measurement],
) -> List[Tuple[date, float]]:
    return _generate_prediction(measurements, "deepesn")


def generate_prediction_subreservoir(
    measurements: List[Measurement],
) -> List[Tuple[date, float]]:
    return _generate_prediction(measurements, "deepsubreservoiresn")


def generate_prediction_esn_base(
    measurements: List[Measurement],
) -> List[Tuple[date, float]]:
    return _generate_prediction(measurements, "esnbase")


def _generate_prediction(
    measurements: List[Measurement], model: str
) -> List[Tuple[date, float]]:
    """Creates prediction for given measurements.
    Time range of generated predictions is the same as time range of measurements,
    i.e. it starts the day after the last measurement and lasts for the same number of days as
    the difference between first and last measurement.
    :returns list of tuples (date, value)"""
    first_date = min(m.date for m in measurements)
    transformed_measurements = _transform_measurements(first_date, measurements)
    x, y = _interpolate_missing_days(transformed_measurements)
    predictions = _predict(x, y, model)
    return _transform_predictions(first_date, predictions)


def _transform_measurements(
    first_date: datetime.date, measurements: List[Measurement]
) -> List[tuple]:
    def date_to_offset(date):
        return (date - first_date).days

    return sorted((date_to_offset(m.date), m.value) for m in measurements)


def _choose_spline_degree(data_size: int) -> int:
    if data_size == 5:
        return 3
    if data_size > 5:
        return 5
    return data_size - 1


def _interpolate_missing_days(
    measurements: List[tuple],
) -> Tuple[np.ndarray, np.ndarray]:
    x, y = unzip(measurements)
    spline_degree = _choose_spline_degree(len(x))
    spline_fun = make_interp_spline(x, y, k=3)
    dense_x = np.arange(x[0], x[-1] + AUGMENTATION_DENSITY, AUGMENTATION_DENSITY)
    dense_y = spline_fun(dense_x)
    dense_y = dense_y.astype(float)
    return dense_x, dense_y


def _to_tensor(array: np.ndarray) -> Tensor:
    reshaped = array.reshape((-1, 1, 1))
    return torch.from_numpy(reshaped).to(device)


def _predict(day_offsets: np.ndarray, values: np.ndarray, model) -> List[tuple]:
    day_offsets_pred = np.arange(
        day_offsets[-1],
        day_offsets[-1] + len(day_offsets) / AUGMENTATION_CONST / 2,
        AUGMENTATION_DENSITY,
    )
    x, y = _to_tensor(values[:-1]), _to_tensor(values[1:])
    esn = _choose_model(model, len(day_offsets))
    esn.fit(x, y)
    y_pred = []
    p = torch.from_numpy(values[-1:])
    p = torch.reshape(p, (1, 1, 1))
    n = len(day_offsets_pred)
    for _ in range(n):
        p = esn(p)
        p = torch.reshape(p, (1, 1, 1))
        y_pred.append(p.item())
    return list(
        zip(
            np.around(day_offsets_pred[::AUGMENTATION_CONST]),
            y_pred[::AUGMENTATION_CONST],
        )
    )


def _transform_predictions(first_date: datetime.date, predictions: List[tuple]):
    def offset_to_date(day_offset):
        return first_date + datetime.timedelta(days=day_offset)

    return [(offset_to_date(off), val) for off, val in predictions]


def _choose_model(model_name: str, data_size: int):
    if model_name == "deepesn":
        return DeepESN(
            1,
            100,
            initializer=WeightInitializer(),
            num_layers=3,
            bias=False,
            activation=activation.relu(leaky_rate=0.4),
            transient=data_size // 2,
        )
    elif model_name == "deepsubreservoiresn":
        return DeepSubreservoirESN(
            1,
            1,
            initializer=SubreservoirWeightInitializer(subreservoir_size=90),
            num_layers=2,
            bias=False,
            activation=activation.relu(leaky_rate=0.4),
            transient=data_size // 2,
        )
    elif model_name == "esnbase":
        return ESNBase(
            reservoir=DeepESNCell(
                1,
                hidden_size=100,
                bias=False,
                activation=activation.relu(leaky_rate=0.4),
            ),
            readout=SVDReadout(100, 1),
            transient=(data_size * 2) // 3,
        )
    raise Exception("Not supported model")
