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

from db.treatment import create_treatment_for_patient


class TreatmentForm(QDialog):
    def __init__(self, parent, patient):
        QDialog.__init__(self)
        self.patient = patient
        self.parent = parent

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.saveForm)

        self.spin_boxes = []
        self.form_layout = QFormLayout()
        treatment_layout = QHBoxLayout()

        self.date_field = QDateEdit()

        spin_box = QDoubleSpinBox()
        spin_box.setRange(0.0, 1.0)
        spin_box.setSingleStep(0.1)

        self.treatment_field = spin_box

        treatment_layout.addWidget(self.date_field)
        treatment_layout.addWidget(self.treatment_field)

        self.form_layout.addRow(treatment_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(buttons_layout)

    def saveForm(self):
        self.date = self.date_field.date().toPython()
        self.value = round(self.treatment_field.value(), 1)

        if any([self.date == m.date for m in self.patient.treatments]):
            QMessageBox.warning(
                self,
                "Dodawanie pomiaru",
                "Istnieje pomiar z tą datą",
            )
            return
        treatment = create_treatment_for_patient(self.patient, self.date, self.value)
        self.parent.addTreatment(treatment)