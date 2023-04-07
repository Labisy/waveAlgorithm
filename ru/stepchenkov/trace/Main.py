import sys
import traceback

from PyQt5.QtWidgets import QApplication

from ru.stepchenkov.trace.window.MainWindow import MainWindow

"""
    Ловим ошибки.
"""


def exception_hook(exc_type, exc_value, exc_tb) -> None:
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Err: ", tb)


"""
    Запуск.
"""
if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    ex = MainWindow()
    app.exec_()
    del ex, app


def start():
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    ex = MainWindow()
    app.exec_()
    del ex, app
