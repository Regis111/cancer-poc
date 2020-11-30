from PySide2.QtWidgets import (
    QWidget,
    QDoubleSpinBox,
    QDateTimeEdit,
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
        self.add_field_button.clicked.connect(self.addRow)

        self.remove_field_button = QPushButton("Usuń pomiar")
        self.remove_field_button.clicked.connect(self.removeRow)

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.saveForm)

        self.spin_boxes = []
        self.form_layout = QFormLayout()
        self.addRow()

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.add_field_button)
        self.buttons_layout.addWidget(self.remove_field_button)
        self.buttons_layout.addWidget(self.save_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

    def saveForm(self):
        ith_layout = lambda i: self.form_layout.itemAt(i).layout()
        take_date = lambda layout: layout.itemAt(0).widget().dateTime().toPython()
        take_measurement = lambda layout: layout.itemAt(1).widget().value()
        layouts = [ith_layout(i) for i in range(self.form_layout.rowCount())]
        dates_values = [(take_date(l), take_measurement(l)) for l in layouts]
        create_measurements_for_patient(self.patient, dates_values)

    def addRow(self):
        measurement_layout = QHBoxLayout()
        measurement_layout.addWidget(self.datetime_field())
        measurement_layout.addWidget(self.measurement_field())
        self.form_layout.addRow(measurement_layout)

    def removeRow(self):
        row_count = self.form_layout.rowCount()
        self.form_layout.removeRow(row_count - 1)

    def measurement_field(self):
        spin_box = QDoubleSpinBox()
        spin_box.setRange(0.0, 100.0)
        spin_box.setSingleStep(0.1)
        return spin_box

    def datetime_field(self):
        date = QDateTimeEdit()
        return date
