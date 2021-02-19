from prediction.util import date_to_offset, interpolate_missing_days, offset_to_date
from data_model.Measurement import Measurement
from data_model.Prediction import Prediction
import logging
from typing import List
from prediction.util import pairwise
import datetime

from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from util import unzip

from db.config import DATETIME_FORMAT

logging.getLogger("matplotlib").setLevel(logging.WARNING)
from matplotlib.figure import Figure


class PredictionsView(QWidget):
    """View for drawing chosen already generated predictions"""

    def __init__(
        self,
        patient_name: str,
        measurements: List[Measurement],
        predictions: List[Prediction],
    ):
        QWidget.__init__(self)
        self.colors = [
            "tab:blue",
            "tab:orange",
            "tab:green",
            "tab:red",
            "tab:purple",
            "tab:brown",
            "tab:pink",
            "tab:gray",
            "tab:olive",
            "tab:cyan",
        ]
        self.setWindowTitle("Widok predykcji")
        self.resize(1500, 800)

        self.measurements = measurements
        self.predictions = predictions

        logging.debug("Predictions number: %d", len(self.predictions))

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))

        self.axes = self.canvas.figure.subplots()

        measurements_dates = [m.date for m in self.measurements]
        first_date = min(measurements_dates)
        measurements_values = [m.value for m in self.measurements]

        def augment_data():
            measurement_offsets = [
                date_to_offset(first_date, d) for d in measurements_dates
            ]
            offset_values = [*zip(measurement_offsets, measurements_values)]
            dense_offsets, dense_values = interpolate_missing_days(offset_values)
            dense_dates = [offset_to_date(first_date, o) for o in dense_offsets]
            dense_data = [
                (d, v)
                for (d, v) in zip(dense_dates, dense_values)
                if d not in measurements_dates
            ]
            dense_dates, dense_values = unzip(dense_data)
            return dense_dates, dense_values

        diffs = [d2 - d1 for d1, d2 in pairwise(measurements_dates)]
        frequency = sum(diffs, datetime.timedelta(days=0)) / len(diffs)

        dense_dates, dense_values = (
            augment_data() if frequency > datetime.timedelta(days=1) else ([], [])
        )
        self.axes.plot(
            dense_dates,
            dense_values,
            "c",
            markersize=8,
            label="Pomiary zaugmentowane",
        )
        self.axes.plot(
            measurements_dates,
            measurements_values,
            "k.",
            markersize=12,
            label="Pomiary",
        )
        self.axes.set_title(f"Rozwój nowotworu pacjent-a {patient_name}")
        for prediction in self.predictions:
            color = self.colors.pop()
            dates = [pv.date for pv in prediction.prediction_values]
            prediction_values = [pv.value for pv in prediction.prediction_values]
            self.axes.plot(
                dates,
                prediction_values,
                ".",
                markersize=4,
                color=color,
                label=f"id{prediction.db_id} {prediction.method} {prediction.datetime_created.strftime(DATETIME_FORMAT)}",
            )
        self.axes.legend()
