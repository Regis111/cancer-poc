from datetime import date, timedelta
from typing import Tuple, List

import numpy as np

from scipy.interpolate import make_interp_spline
from data_model.Measurement import Measurement
from util import unzip
import operator

AUGMENTATION_CONST = 10
AUGMENTATION_DENSITY = 1 / AUGMENTATION_CONST


def date_to_offset(first_date: date, date: date) -> float:
    return round((date - first_date).days * 0.1, 1)


def offset_to_date(first_date: date, t: int) -> date:
    return first_date + timedelta(days=int(round(t / 0.1)))


def transform_measurements(
    first_date: date, measurements: List[Measurement]
) -> List[tuple]:
    return sorted(
        [(date_to_offset(first_date, m.date), m.value) for m in measurements],
        key=operator.itemgetter(0),
    )


def interpolate_missing_days(
    measurements: List[tuple],
) -> Tuple[np.ndarray, np.ndarray]:
    def choose_spline_degree(data_size: int) -> int:
        if data_size == 5:
            return 3
        if data_size > 5:
            return 5
        return data_size - 1

    x, y = unzip(measurements)
    spline_degree = choose_spline_degree(len(x))
    print("i", x)
    spline_fun = make_interp_spline(x, y, k=spline_degree)
    dense_x = np.arange(x[0], x[-1] + AUGMENTATION_DENSITY, AUGMENTATION_DENSITY)
    dense_y = spline_fun(dense_x)
    dense_y = dense_y.astype(float)
    return dense_x, dense_y


def transform_predictions(first_date: date, predictions: List[tuple]):
    return sorted(
        [(offset_to_date(first_date, off), val) for off, val in predictions],
        key=operator.itemgetter(0),
    )
