from PySide2.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox,
)
from db.patient import create_patient


class PatientForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.firstname = QLineEdit()
        self.firstname.setMaxLength(20)
        self.surname = QLineEdit()
        self.surname.setMaxLength(20)

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.save_form)

        self.layout = QFormLayout()
        self.layout.addRow("Imię", self.firstname)
        self.layout.addRow("Nazwisko", self.surname)
        self.layout.addRow(self.save_button)

        self.setLayout(self.layout)

    def save_form(self):
        if not self.firstname.text().isalpha() or not self.surname.text().isalpha():
            QMessageBox.critical(
                self,
                "QMessageBox.critical()",
                "Imię i Nazwisko musi być złożone wyłącznie z liter",
                QMessageBox.Abort,
            )
        else:
            create_patient(self.firstname.text(), self.surname.text())
