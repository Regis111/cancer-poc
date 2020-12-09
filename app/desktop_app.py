import sys
from PySide2.QtWidgets import QApplication

from db.initialize import init
from qt_classes.window import Window


if __name__ == "__main__":
    init()
    app = QApplication(sys.argv)
    main = Window()

    sys.exit(app.exec_())
