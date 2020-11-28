from PySide2.QtWidgets import (
    QWidget,
    QDoubleSpinBox,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from db.measurement import create_measurements_for_patient
from datetime import date


class MeasurementsForm(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        self.patient = patient

        self.add_field_button = QPushButton("Dodaj pomiar")
        self.add_field_button.clicked.connect(self.addField)

        self.remove_field_button = QPushButton("Usuń pomiar")
        self.remove_field_button.clicked.connect(self.removeField)

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.saveForm)

        self.spin_boxes = []
        self.form_layout = QFormLayout()
        self.addField()

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.add_field_button)
        self.buttons_layout.addWidget(self.remove_field_button)
        self.buttons_layout.addWidget(self.save_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

    def saveForm(self):
        today = date.today()
        ith_value = (
            lambda i: self.form_layout.itemAt(i, QFormLayout.FieldRole).widget().value()
        )
        dates_values = [
            (today, ith_value(i)) for i in range(self.form_layout.rowCount())
        ]
        create_measurements_for_patient(self.patient, dates_values)

    def addField(self):
        self.form_layout.addRow(self.field())

    def removeField(self):
        row_count = self.form_layout.rowCount()
        self.form_layout.removeRow(row_count - 1)

    def field(self):
        spin_box = QDoubleSpinBox()
        spin_box.setRange(0.0, 100.0)
        spin_box.setSingleStep(0.1)
        return spin_box
