import sys
import logging

from PySide2.QtWidgets import QApplication

from db.initialize import init
from frontend.window import Window

import qdarkstyle

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    init()

    app = QApplication(sys.argv)

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    main = Window()

    sys.exit(app.exec_())
