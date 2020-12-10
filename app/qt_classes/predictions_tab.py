import logging
from datetime import datetime
from typing import List, Dict

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QAction,
    QToolBar,
    QListWidget,
)

from data_model.PredictionValue import PredictionValue
from db.prediction import delete_prediction_for_patient
from qt_classes.prediction_form import PredictionForm
from qt_classes.prediction_view import PredictionView

logging.basicConfig(level=logging.DEBUG)


class PredictionsTab(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        self.patient = patient

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)

        add_prediction = QAction(QIcon("icon/plus.png"), "Dodaj pomiar", self)
        add_prediction.triggered.connect(self.addPredictionForm)
        add_prediction.setStatusTip("Dodaj pomiary")
        self.toolbar.addAction(add_prediction)

        delete_prediction = QAction(QIcon("icon/d1.png"), "Usuń pomiar", self)
        delete_prediction.triggered.connect(self.deletePrediction)
        delete_prediction.setStatusTip("Usuń pomiar")
        self.toolbar.addAction(delete_prediction)

        draw_predictions = QAction(QIcon("icon/trend.png"), "Rysuj predykcje", self)
        # draw_predictions.triggered.connect(self.deleteCurrentMeasurement)
        draw_predictions.setStatusTip("Rysuj predykcje")
        self.toolbar.addAction(draw_predictions)

        self.predictions_list = QListWidget()
        self.fillList()

        main_layout = QHBoxLayout(self)
        main_layout.setMenuBar(self.toolbar)
        main_layout.addWidget(self.predictions_list)

    def fillList(self):
        for prediction_datetime in self.patient.predictions:
            self.predictions_list.addItem(prediction_datetime.isoformat())

    def addPredictionForm(self):
        self.predicion_form = PredictionForm(self.patient)
        self.predicion_form.exec()
        self.reload()

    def deletePrediction(self):
        prediction_datetime_iso = self.predictions_list.currentItem().text()
        prediction_datetime = datetime.fromisoformat(prediction_datetime_iso)
        delete_prediction_for_patient(self.patient, prediction_datetime)
        self.reload()

    def showPredictions(self):
        chosen_predictions_datetimes: List[
            datetime
        ] = self.predictions_list.selectedItems()
        chosen_predictions: Dict[datetime, List[PredictionValue]] = {
            prediction_datetime: prediction_value_list
            for prediction_datetime, prediction_value_list in self.patient.predictions.items()
            if prediction_datetime in chosen_predictions_datetimes
        }
        self.predictions_view = PredictionView(
            self.patient.measurements, chosen_predictions
        )
        self.predictions_view.show()

    def reload(self):
        self.predictions_list.clear()
        self.fillList()
