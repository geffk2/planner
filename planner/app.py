import sys
from planner.main_window import MainWindow
from PyQt5.QtWidgets import QApplication

main_window = None


def run():
    global main_window
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
