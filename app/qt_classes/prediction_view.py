from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import numpy as np


class PredictionView(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.static_canvas)
        self.layout.addWidget(NavigationToolbar(self.static_canvas, self))
        self._static_ax = self.static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self.setLayout(self.layout)
