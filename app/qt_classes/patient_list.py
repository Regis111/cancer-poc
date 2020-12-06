from PySide2.QtWidgets import (
    QWidget,
    QTableWidget,
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

from qt_classes.patient_form import PatientForm

import logging

logging.basicConfig(level=logging.DEBUG)


class PatientListView(QWidget):
    columns = ["Identyfikator", "Imię", "Nazwisko"]

    def __init__(self):
        QWidget.__init__(self)

        self.items = 0

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)

        btn_ac_adduser = QAction(QIcon("icon/add1.jpg"), "Add Patient", self)
        btn_ac_adduser.triggered.connect(self.addPatientForm)
        btn_ac_adduser.setStatusTip("Add Student")
        self.toolbar.addAction(btn_ac_adduser)

        btn_ac_delete = QAction(QIcon("icon/d1.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.deleteCurrentPatient)
        btn_ac_delete.setStatusTip("Delete User")
        self.toolbar.addAction(btn_ac_delete)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.verticalHeader().setVisible(False)

        self.data = get_all_patients()

        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.fillTable()

        # whole layout
        layout = QHBoxLayout()
        layout.setMenuBar(self.toolbar)
        layout.addWidget(self.table)

        self.setLayout(layout)

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
            self.addPatient(self.patient_form.patient)
            logging.debug(f"Patient {self.patient_form.patient} added")

    def deleteCurrentPatient(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(
                self, "Usuwanie pacjenta", f"Brak danych w tabeli",
            )
            return

        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(
                self, "Usuwanie pacjenta", f"Brak wskazania na pacjenta",
            )
            return

        patient = self.data[current_row]
        answer = QMessageBox.question(
            self,
            "Usuwanie pacjenta",
            f"Czy na pewno chcesz usunąć pacjenta {patient}?",
        )
        if answer == QMessageBox.Yes:
            delete_patient(patient)
            self.table.removeRow(current_row)
            logging.debug("Deleting PatientForm")
