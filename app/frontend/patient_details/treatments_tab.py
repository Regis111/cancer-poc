from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QHBoxLayout,
    QAction,
    QToolBar,
    QMessageBox,
)
import logging
from frontend.patient_details.treatment_form import TreatmentForm
from db.treatment import delete_treatment_for_patient


class TreatmentsTab(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        self.patient = patient

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)

        add_treatment = QAction(
            QIcon("resources/icon/plus.png"), "Podaj lekarstwo", self
        )
        add_treatment.triggered.connect(self.addTreatmentForm)
        add_treatment.setStatusTip("Dodaj pomiary")
        self.toolbar.addAction(add_treatment)

        delete_treatment = QAction(
            QIcon("resources/icon/trash-bin.png"), "Usuń podanie lekarstwa", self
        )
        delete_treatment.triggered.connect(self.deleteCurrentTreatment)
        delete_treatment.setStatusTip("Usuń pomiar")
        self.toolbar.addAction(delete_treatment)

        self.table = QTableWidget()
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(["Data", "Zawartość lekarstwa"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fillTable(patient.treatments)

        main_layout = QHBoxLayout(self)
        main_layout.setMenuBar(self.toolbar)
        main_layout.addWidget(self.table)

    def addTreatmentForm(self):
        logging.debug("Entering TreatmentForm of patient %s", self.patient)
        self.treatment_form = TreatmentForm(self, self.patient)
        self.treatment_form.show()

    def fillTable(self, treatments):
        for tr in treatments:
            self.addTreatment(tr)

    def addTreatment(self, treatment):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(
            row_count, 0, self.tableWidgetItem(treatment.date.isoformat())
        )
        self.table.setItem(row_count, 1, self.tableWidgetItem(str(treatment.amount)))

    def tableWidgetItem(self, value):
        item = QTableWidgetItem(value)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def deleteCurrentTreatment(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(
                self,
                "Usuwanie podania lekarstwa",
                "Brak danych w tabeli",
            )
            return
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(
                self,
                "Usuwanie lekarstwa",
                "Brak wskazania na żaden pomiar",
            )
            return
        treatment = self.patient.treatments[current_row]
        answer = QMessageBox.question(
            self,
            "Usuwanie pomiaru",
            f"Czy na pewno chcesz usunąć podanie lekarstwa {treatment}?",
        )
        if answer == QMessageBox.Yes:
            delete_treatment_for_patient(self.patient, treatment)
            self.table.removeRow(current_row)
            logging.debug(f"Deleting {treatment}")
