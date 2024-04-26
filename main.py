import sys
import os
from PySide6.QtWidgets import QApplication
from interface.MainWindow import MainWindow

if __name__ == '__main__':
    try:
        os.mkdir('ext_archive')
    except FileExistsError:
        pass
    app = QApplication()
    window = MainWindow()

    window.show()
    sys.exit(app.exec())
