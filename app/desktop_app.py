import sys
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QLineEdit,
    QFormLayout,
    QDialog,
    QMessageBox,
)

from db import initialize


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.width = 800
        self.height = 600

        self.resize(self.width, self.height)
        self.setStartView()

    def setStartView(self):
        self.widget = StartView(self.width, self.height)
        self.setCentralWidget(self.widget)
        self.widget.start_button.clicked.connect(self.setListView)
        self.show()

    def setListView(self):
        self.widget = PatientListView()
        self.setCentralWidget(self.widget)
        self.widget.table.cellDoubleClicked.connect(self.setDetailsView)
        self.widget.add_patient.clicked.connect(self.openNewPatientForm)
        self.show()

    def setDetailsView(self, row, column):
        self.widget = PatientDetailsView()
        self.setCentralWidget(self.widget)
        self.widget.back_button.clicked.connect(self.setListView)
        self.show()

    def openNewPatientForm(self):
        print("openNewPatientForm")
        patient_form = NewPatientForm(self)
        patient_form.show()
        # self.hide()


class StartView(QWidget):
    def __init__(self, width, height):
        super(StartView, self).__init__()

        self.width = width
        self.height = height

        self.button_size = (150, 50)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(
            (self.width / 2) - (self.button_size[0] / 2) - 125,
            (self.height / 2) - (self.button_size[1] / 2),
            self.button_size[0],
            self.button_size[1],
        )

        self.help_button = QPushButton("Help", self)
        self.help_button.setGeometry(
            (self.width / 2) - (self.button_size[0] / 2) + 125,
            (self.height / 2) - (self.button_size[1] / 2),
            self.button_size[0],
            self.button_size[1],
        )


class PatientListView(QWidget):
    def __init__(self, parent=None):
        super(PatientListView, self).__init__(parent)

        self.items = 0

        # left column table
        self.table = QTableWidget()
        self.table.setColumnCount(2)

        self._data = {
            "Water": 24.5,
            "Electricity": 55.1,
            "Rent": 850.0,
            "Supermarket": 230.4,
            "Internet": 29.99,
            "Bars": 21.85,
            "Public transportation": 60.0,
            "Coffee": 22.45,
            "Restaurants": 120,
        }

        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.fill_table()

        # right column
        self.add_patient = QPushButton("Dodaj nowego pacjenta")
        self.right = QVBoxLayout()
        self.right.setMargin(20)
        self.right.addWidget(self.add_patient)

        # whole layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, price in data.items():
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(desc))
            self.table.setItem(self.items, 1, QTableWidgetItem(str(price)))
            self.items += 1


class PatientDetailsView(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.items = 0

        self._data = {
            "Water": 24.5,
            "Electricity": 55.1,
            "Rent": 850.0,
            "Supermarket": 230.4,
            "Internet": 29.99,
            "Bars": 21.85,
            "Public transportation": 60.0,
            "Coffee": 22.45,
            "Restaurants": 120,
        }

        self.table = QTableWidget()
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # right column
        self.back_button = QPushButton("Wstecz")

        self.right = QVBoxLayout()
        self.right.setMargin(20)
        self.right.addWidget(self.back_button)
        self.right.addWidget(QPushButton("Dodaj pomiar"))
        self.right.addWidget(QPushButton("Zobacz Predykcję"))

        # whole layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

        self.fill_table()

    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, price in data.items():
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(desc))
            self.table.setItem(self.items, 1, QTableWidgetItem(str(price)))

            self.items += 1


class NewPatientForm(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

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
        firstname_str = self.firstname.text()
        surname_str = self.surname.text()
        if not firstname_str or not surname_str:
            reply = QMessageBox.critical(
                self,
                "QMessageBox.critical()",
                "XDDDD",
                QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore,
            )
        else:
            ## save and exit
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Window()

    sys.exit(app.exec_())
