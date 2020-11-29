from PySide2.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from PySide2.QtCore import Qt
import logging
from datetime import date

logging.basicConfig(level=logging.DEBUG)


class PatientDetailsView(QWidget):
    columns = ["Data", "Wartość"]

    def __init__(self, patient):
        QWidget.__init__(self)
        self.items = 0

        self.date_strftime = "%d/%m/%Y"

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))

        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fillTable(patient.measurements)

        # right column
        self.back_button = QPushButton("Wstecz")
        self.add_measurements_button = QPushButton("Dodaj pomiar")
        self.prediction_button = QPushButton("Zobacz Predykcję")

        self.right = QVBoxLayout()
        self.right.setMargin(20)
        self.right.addWidget(self.back_button)
        self.right.addWidget(self.add_measurements_button)
        self.right.addWidget(self.prediction_button)

        # whole layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

    def fillTable(self, measurements):
        for m in measurements:
            self.table.insertRow(self.items)

            self.table.setItem(self.items, 0, self.tableWidgetItem(m.date.isoformat()))
            self.table.setItem(self.items, 1, self.tableWidgetItem(str(m.value)))

            self.items += 1

    def tableWidgetItem(self, value):
        item = QTableWidgetItem(value)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item
