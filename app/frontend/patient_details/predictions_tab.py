from data_model.Prediction import Prediction
import logging
from datetime import datetime
from typing import List, Set

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QAction,
    QToolBar,
    QWidget,
    QTableWidget,
    QAbstractItemView,
    QHeaderView,
    QTableWidgetItem,
    QHBoxLayout,
    QAction,
    QToolBar,
    QMessageBox,
)

from db.prediction import delete_prediction_for_patient
from db.config import DATETIME_FORMAT
from frontend.patient_details.prediction_form import PredictionForm
from frontend.patient_details.prediction_view import PredictionsView


class PredictionsTab(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        self.patient = patient
        self.prediction_views = set()

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)

        add_prediction = QAction(QIcon("icon/plus.png"), "Dodaj predykcję", self)
        add_prediction.triggered.connect(self.addPredictionForm)
        add_prediction.setStatusTip("Dodaj pomiary")
        self.toolbar.addAction(add_prediction)

        delete_prediction = QAction(QIcon("icon/d1.png"), "Usuń predykcję", self)
        delete_prediction.triggered.connect(self.deletePrediction)
        delete_prediction.setStatusTip("Usuń pomiar")
        self.toolbar.addAction(delete_prediction)

        draw_predictions = QAction(QIcon("icon/trend.png"), "Rysuj predykcje", self)
        draw_predictions.triggered.connect(self.showPredictions)
        draw_predictions.setStatusTip("Rysuj predykcje")
        self.toolbar.addAction(draw_predictions)

        self.table = QTableWidget()
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(["Data", "Metoda"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.fillTable()

        main_layout = QHBoxLayout(self)
        main_layout.setMenuBar(self.toolbar)
        main_layout.addWidget(self.table)

    def fillTable(self):
        for p in self.patient.predictions:
            self.addPrediction(p)

    def addPrediction(self, prediction: Prediction):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(
            row_count,
            0,
            self.tableWidgetItem(prediction.datetime_created.strftime(DATETIME_FORMAT)),
        )
        self.table.setItem(row_count, 1, self.tableWidgetItem(prediction.method))

    def tableWidgetItem(self, value):
        item = QTableWidgetItem(value)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def addPredictionForm(self):
        self.predicion_form = PredictionForm(self, self.patient)
        self.predicion_form.exec()

    def deletePrediction(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(
                self,
                "Usuwanie predykcji",
                f"Brak danych w tabeli",
            )
            return
        prediction_datetime = datetime.fromisoformat(
            self.table.item(current_row, 0).text()
        )
        delete_prediction_for_patient(self.patient, prediction_datetime)
        self.table.removeRow(current_row)

    def showPredictions(self):
        logging.debug(
            "All predictions %s",
            [(p.method, p.datetime_created) for p in self.patient.predictions],
        )
        selected_rows = set([ind.row() for ind in self.table.selectedIndexes()])
        logging.debug("%s", selected_rows)
        chosen_predictions_datetimes: List[datetime] = [
            datetime.strptime(self.table.item(ind, 0).text(), DATETIME_FORMAT)
            for ind in selected_rows
        ]
        logging.debug("Selected datetimes from table: %s", chosen_predictions_datetimes)
        chosen_predictions: Set[Prediction] = {
            prediction
            for prediction in self.patient.predictions
            if prediction.datetime_created in chosen_predictions_datetimes
        }
        logging.debug(
            "Selected predictions to graph: %s %d %s",
            chosen_predictions,
            len(chosen_predictions),
            type(chosen_predictions),
        )
        predictions_view = PredictionsView(
            self.patient.measurements, chosen_predictions
        )
        predictions_view.show()
        self.prediction_views.add(predictions_view)
        logging.debug("Prediction views %s", self.prediction_views)
