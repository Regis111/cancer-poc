from PySide2.QtWidgets import (
    QWidget,
    QDialog,
    QDoubleSpinBox,
    QDateTimeEdit,
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

        self.datetime_field = QDateTimeEdit()

        spin_box = QDoubleSpinBox()
        spin_box.setRange(0.0, 10000.0)
        spin_box.setSingleStep(0.1)

        self.measurement_field = spin_box

        measurement_layout.addWidget(self.datetime_field)
        measurement_layout.addWidget(self.measurement_field)

        self.form_layout.addRow(measurement_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.exit_button)
        buttons_layout.addWidget(self.save_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(buttons_layout)

        self.setLayout(self.layout)

    def saveForm(self):
        self.date = self.datetime_field.date().toPython()
        self.value = self.measurement_field.value()
        measurement = create_measurement_for_patient(
            self.patient, self.date, self.value
        )
        self.parent.addMeasurement(measurement)
