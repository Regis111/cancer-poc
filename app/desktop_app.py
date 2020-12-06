import logging
import sys

from PySide2.QtWidgets import QApplication, QMainWindow

from db.initialize import init
from qt_classes.measurements_form import MeasurementsForm
from qt_classes.patient_details import PatientDetailsView
from qt_classes.patient_form import PatientForm
from qt_classes.patient_list import PatientListView
from qt_classes.prediction_view import PredictionView
from qt_classes.start import StartView

logging.basicConfig(level=logging.DEBUG)


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.width = 800
        self.height = 600

        self.resize(self.width, self.height)
        self.setListView()

    def setListView(self):
        logging.debug("Entering ListView")
        self.widget = PatientListView()
        self.setCentralWidget(self.widget)
        self.widget.table.cellDoubleClicked.connect(
            lambda row, column: self.setDetailsView(self.widget.data[row])
        )
        self.show()

    def setDetailsView(self, patient):
        logging.debug("Entering DetailsView of %s", patient)
        self.widget = PatientDetailsView(patient)
        self.setCentralWidget(self.widget)
        self.widget.back_button.clicked.connect(self.setListView)
        self.show()


if __name__ == "__main__":
    init()
    app = QApplication(sys.argv)
    main = Window()

    sys.exit(app.exec_())
