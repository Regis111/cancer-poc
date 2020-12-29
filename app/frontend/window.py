import logging

from PySide2.QtWidgets import QMainWindow

from frontend.patient_details.patient_details import PatientDetailsView
from frontend.patient_list.patient_list import PatientListView


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.width = 800
        self.height = 600
        self.setWindowTitle("Cancer Prediction Tool")

        self.resize(self.width, self.height)
        self.setListView()

    def setListView(self):
        logging.debug("Entering ListView")
        self.widget = PatientListView()
        self.setCentralWidget(self.widget)
        self.widget.table.cellDoubleClicked.connect(
            lambda row, _: self.setDetailsView(self.widget.data[row])
        )
        self.show()

    def setDetailsView(self, patient):
        logging.debug("Entering DetailsView of %s", patient)
        self.widget = PatientDetailsView(patient)
        self.setCentralWidget(self.widget)
        self.widget.back_button.clicked.connect(self.setListView)
        self.show()
