import logging

from PySide2.QtWidgets import (
    QDialog,
    QDoubleSpinBox,
    QDateEdit,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)

from db.measurement import create_measurement_for_patient


class MeasurementsForm(QDialog):
    def __init__(self, parent, patient):
        QDialog.__init__(self)
        self.patient = patient
        self.parent = parent

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.saveForm)

        self.exit_button = QPushButton("Wyjdź")
        self.exit_button.clicked.connect(self.accept)

        self.spin_boxes = []
        self.form_layout = QFormLayout()
        measurement_layout = QHBoxLayout()

        self.date_field = QDateEdit()

        spin_box = QDoubleSpinBox()
        spin_box.setRange(0.0, 10000.0)
        spin_box.setSingleStep(0.1)

        self.measurement_field = spin_box

        measurement_layout.addWidget(self.date_field)
        measurement_layout.addWidget(self.measurement_field)

        self.form_layout.addRow(measurement_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.exit_button)
        buttons_layout.addWidget(self.save_button)

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(buttons_layout)

    def saveForm(self):
        self.date = self.date_field.date().toPython()
        self.value = round(self.measurement_field.value(), 1)

        if any([self.date == m.date for m in self.patient.measurements]):
            QMessageBox.warning(
                self,
                "Dodawanie pomiaru",
                "Istnieje pomiar z tą datą",
            )
            return
        measurement = create_measurement_for_patient(
            self.patient, self.date, self.value
        )
        self.parent.addMeasurement(measurement)
