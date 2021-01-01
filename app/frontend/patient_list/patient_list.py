from PySide2.QtWidgets import (
    QWidget,
    QTableWidget,
    QAbstractItemView,
    QHeaderView,
    QTableWidgetItem,
    QHBoxLayout,
    QAction,
    QToolBar,
    QMessageBox,
    QDialog,
)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from db.patient import get_all_patients, delete_patient

import logging

from frontend.patient_list.patient_form import PatientForm


class PatientListView(QWidget):
    columns = ["Identyfikator", "Imię", "Nazwisko"]

    def __init__(self):
        QWidget.__init__(self)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)

        btn_ac_adduser = QAction(QIcon("resources/icon/add1.jpg"), "Add Patient", self)
        btn_ac_adduser.triggered.connect(self.addPatientForm)
        btn_ac_adduser.setStatusTip("Add Student")
        self.toolbar.addAction(btn_ac_adduser)

        btn_ac_delete = QAction(QIcon("resources/icon/d1.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.deleteCurrentPatient)
        btn_ac_delete.setStatusTip("Delete User")
        self.toolbar.addAction(btn_ac_delete)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnCount(len(self.columns))
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(self.columns)

        self.reload()

        layout = QHBoxLayout(self)
        layout.setMenuBar(self.toolbar)
        layout.addWidget(self.table)

    def fillTable(self):
        for patient in self.data:
            self.addPatient(patient)

    def addPatient(self, patient):
        ind = self.table.rowCount()
        self.table.insertRow(ind)
        self.table.setItem(ind, 0, self.tableWidgetItem(str(patient.db_id)))
        self.table.setItem(ind, 1, self.tableWidgetItem(patient.name))
        self.table.setItem(ind, 2, self.tableWidgetItem(patient.surname))

    def tableWidgetItem(self, value):
        item = QTableWidgetItem(value)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def addPatientForm(self):
        logging.debug("Entering PatientForm")
        self.patient_form = PatientForm()
        answer = self.patient_form.exec()
        if answer == QDialog.Accepted:
            self.reload()
            logging.debug(f"Patient {self.patient_form.patient} added")

    def deleteCurrentPatient(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(
                self,
                "Usuwanie pacjenta",
                "Brak danych w tabeli",
            )
            return

        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(
                self,
                "Usuwanie pacjenta",
                "Brak wskazania na pacjenta",
            )
            return

        patient = self.data[current_row]
        answer = QMessageBox.question(
            self,
            "Usuwanie pacjenta",
            f"Czy na pewno chcesz usunąć pacjenta {patient}?",
        )
        if answer == QMessageBox.Yes:
            delete_patient(patient)
            self.reload()
            logging.debug("Deleting PatientForm")

    def reload(self):
        self.table.setRowCount(0)
        self.data = get_all_patients()
        self.fillTable()
