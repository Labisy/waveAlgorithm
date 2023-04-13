from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtWidgets import QMainWindow

from ru.stepchenkov.trace.window.PathController import MainWindowInit
from ru.stepchenkov.trace.types import ColorType
from ru.stepchenkov.trace.types import TextType


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.mainWidget = MainWindowInit(self)

        self.setWindowTitle(TextType.task)
        self.setStyleSheet(f"background-color: {ColorType.white}")

        self.setCentralWidget(self.mainWidget)
        QTimer.singleShot(1, lambda: self.windowSize())
        self.show()


    def windowSize(self):
        self.setFixedSize(self.mainWidget.layout.sizeHint() + QSize(30, 30))
