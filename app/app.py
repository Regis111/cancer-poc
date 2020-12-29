import sys
from PySide2.QtWidgets import QApplication

from db.initialize import init
from frontend.window import Window

import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    init()
    app = QApplication(sys.argv)
    main = Window()

    sys.exit(app.exec_())
