import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile

from db.initialize import init
from frontend.window import Window

import qdarkstyle
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    init()

    app = QApplication(sys.argv)

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    main = Window()

    sys.exit(app.exec_())
