from PySide2.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide2.QtCore import Qt
from db.patient import get_all_patients, delete_patient

import logging

logging.basicConfig(level=logging.DEBUG)


class PatientListView(QWidget):
    columns = ["Identyfikator", "Imię", "Nazwisko"]

    def __init__(self):
        QWidget.__init__(self)

        self.items = 0

        # left column table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))

        self.data = get_all_patients()

        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.fillTable()

        # right column
        self.add_patient = QPushButton("Dodaj nowego pacjenta")
        self.right = QVBoxLayout()
        self.right.setMargin(20)
        self.right.addWidget(self.add_patient)

        # whole layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

    def fillTable(self):
        for patient in self.data:
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, self.tableWidgetItem(str(patient.db_id)))
            self.table.setItem(self.items, 1, self.tableWidgetItem(patient.name))
            self.table.setItem(self.items, 2, self.tableWidgetItem(patient.surname))
            self.items += 1

    def tableWidgetItem(self, value):
        item = QTableWidgetItem(value)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item
