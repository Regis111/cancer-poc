from qt_classes.measurements_form import MeasurementsForm
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)
from qt_classes.patient_details import PatientDetailsView
from qt_classes.patient_form import PatientForm
from qt_classes.patient_list import PatientListView
from qt_classes.start import StartView

from db.initialize import init

import logging
import sys

logging.basicConfig(level=logging.DEBUG)


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.width = 800
        self.height = 600

        self.resize(self.width, self.height)
        self.setStartView()

    def setStartView(self):
        logging.debug("Entering StartView")
        self.widget = StartView(self.width, self.height)
        self.setCentralWidget(self.widget)
        self.widget.start_button.clicked.connect(self.setListView)
        self.show()

    def setListView(self):
        logging.debug("Entering ListView")
        self.widget = PatientListView()
        self.setCentralWidget(self.widget)
        self.widget.table.cellDoubleClicked.connect(
            lambda row, column: self.setDetailsView(self.widget.data[row])
        )
        self.widget.add_patient.clicked.connect(self.setPatientForm)
        self.show()

    def setPatientForm(self):
        logging.debug("Entering PatientForm")
        self.widget = PatientForm()
        self.setCentralWidget(self.widget)
        self.widget.save_button.clicked.connect(self.setListView)
        self.show()

    def setDetailsView(self, patient):
        logging.debug("Entering DetailsView of %s", patient)
        self.widget = PatientDetailsView(patient)
        self.setCentralWidget(self.widget)
        self.widget.back_button.clicked.connect(self.setListView)
        self.widget.add_measurements.clicked.connect(
            lambda: self.setMeasurementsForm(patient)
        )
        self.show()

    def setMeasurementsForm(self, patient):
        logging.debug("Entering MeasurementForm of patient %s", patient)
        self.widget = MeasurementsForm(patient)
        self.setCentralWidget(self.widget)
        self.widget.save_button.clicked.connect(lambda: self.setDetailsView(patient))
        self.show()


if __name__ == "__main__":
    init()
    app = QApplication(sys.argv)
    main = Window()

    sys.exit(app.exec_())
