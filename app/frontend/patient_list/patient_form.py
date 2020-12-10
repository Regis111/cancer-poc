from PySide2.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox,
    QHBoxLayout,
)

from db.patient import create_patient
import logging




class PatientForm(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.firstname = QLineEdit()
        self.firstname.setMaxLength(20)
        self.surname = QLineEdit()
        self.surname.setMaxLength(20)

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.save_form)

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)

        self.layout = QFormLayout(self)
        self.layout.addRow("Imię", self.firstname)
        self.layout.addRow("Nazwisko", self.surname)
        self.layout.addRow(buttons_layout)

    def save_form(self):
        if not self.firstname.text().isalpha() or not self.surname.text().isalpha():
            QMessageBox.critical(
                self,
                "QMessageBox.critica()",
                "Imię i Nazwisko musi być złożone wyłącznie z liter",
                QMessageBox.Abort,
            )
        else:
            self.patient = create_patient(self.firstname.text(), self.surname.text())
            self.accept()
