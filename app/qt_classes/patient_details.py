from db import measurement
from PySide2.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QTabWidget,
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QAction,
    QToolBar,
    QMessageBox,
)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

from qt_classes.measurements_form import MeasurementsForm
from qt_classes.prediction_view import PredictionView

from db.measurement import delete_measurement_for_patient

import logging

logging.basicConfig(level=logging.DEBUG)


class PatientDetailsView(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        self.setWindowFlags(Qt.Window)

        tab_widget = QTabWidget()
        tab_widget.addTab(PatientDetailsTab(patient), "Szczegóły pacjenta")
        tab_widget.addTab(PatientMeasurementsTab(patient, ("MTD", "mm")), "Pomiary MTD")

        self.back_button = QPushButton("Wróć")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(self.back_button)
        self.setLayout(main_layout)

        self.setWindowTitle(f"Pacjent {patient.name} {patient.surname}")


class PatientDetailsTab(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        name_label = QLabel("Name:")
        name_label_value = QLabel(patient.name)
        name_label_value.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        surname_label = QLabel("Name:")
        surname_label_value = QLabel(patient.surname)
        surname_label_value.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        db_id_label = QLabel("DB id:")
        db_id_label_value = QLabel(str(patient.db_id))
        db_id_label_value.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        main_layout = QVBoxLayout()
        main_layout.addWidget(name_label)
        main_layout.addWidget(name_label_value)
        main_layout.addWidget(surname_label)
        main_layout.addWidget(surname_label_value)
        main_layout.addWidget(db_id_label)
        main_layout.addWidget(db_id_label_value)

        self.setLayout(main_layout)


class PatientMeasurementsTab(QWidget):
    def __init__(self, patient, measurement):
        QWidget.__init__(self)
        self.patient = patient

        measurement_name, measurement_unit = measurement

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)

        btn_ac_adduser = QAction(QIcon("icon/trend.png"), "Zobacz predykcję", self)
        btn_ac_adduser.triggered.connect(self.setPredictionView)
        btn_ac_adduser.setStatusTip("Zobacz predykcję")
        self.toolbar.addAction(btn_ac_adduser)

        btn_ac_search = QAction(QIcon("icon/plus.png"), "Dodaj pomiar", self)
        btn_ac_search.triggered.connect(self.addMeasurementsForm)
        btn_ac_search.setStatusTip("Dodaj pomiary")
        self.toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/d1.png"), "Usuń pomiar", self)
        btn_ac_delete.triggered.connect(self.deleteCurrentMeasurement)
        btn_ac_delete.setStatusTip("Usuń pomiar")
        self.toolbar.addAction(btn_ac_delete)

        self.table = QTableWidget()
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(
            ["Data", f"{measurement_name} [{measurement_unit}]"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.fillTable(patient.measurements)

        self.add_measurements_button = QPushButton("Dodaj pomiar")
        self.prediction_button = QPushButton("Zobacz Predykcję")

        self.right = QVBoxLayout()
        self.right.setMargin(20)
        self.right.addWidget(self.add_measurements_button)
        self.right.addWidget(self.prediction_button)

        main_layout = QHBoxLayout()
        main_layout.setMenuBar(self.toolbar)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def fillTable(self, measurements):
        for m in measurements:
            self.addMeasurement(m)

    def addMeasurement(self, measurement):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(
            row_count, 0, self.tableWidgetItem(measurement.date.isoformat())
        )
        self.table.setItem(row_count, 1, self.tableWidgetItem(str(measurement.value)))

    def tableWidgetItem(self, value):
        item = QTableWidgetItem(value)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def addMeasurementsForm(self):
        logging.debug("Entering MeasurementForm of patient %s", self.patient)
        self.measurement_form = MeasurementsForm(self, self.patient)
        self.measurement_form.show()

    def setPredictionView(self):
        logging.debug("Entering PredictionView")
        self.prediction_view = PredictionView(self.patient)
        self.prediction_view.show()

    def deleteCurrentMeasurement(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(
                self, "Usuwanie pomiaru", f"Brak danych w tabeli",
            )
            return
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(
                self, "Usuwanie pomiaru", f"Brak wskazania na żaden pomiar",
            )
            return
        measurement = self.patient.measurements[current_row]
        answer = QMessageBox.question(
            self,
            "Usuwanie pomiaru",
            f"Czy na pewno chcesz usunąć pomiar {measurement}?",
        )
        if answer == QMessageBox.Yes:
            delete_measurement_for_patient(self.patient, measurement)
            self.table.removeRow(current_row)
            logging.debug(f"Deleting {measurement}")
