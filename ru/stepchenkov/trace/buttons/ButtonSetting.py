from typing import TYPE_CHECKING

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton
from ru.stepchenkov.trace.types import FontType
from ru.stepchenkov.trace.types import ColorType

if TYPE_CHECKING:
    from ru.stepchenkov.trace.window.MainWindow import MainWindowInit


class MenuButton(QPushButton):

    def __init__(self, parent: 'MainWindowInit', text: str) -> None:
        super().__init__(parent)

        '''
            1) Текст на кнопке меню.
            2) font и размер текста.
            3) размеры кнопок.
            4) стили кнопок.
        '''
        self.setText(text)
        self.setFont(QFont(FontType.fontArial, FontType.fontButtonSize))
        self.setFixedSize(180, 40)
        self.setStyleSheet(f"background-color: {ColorType.white};"
                           f"color: {ColorType.black}; "
                           f"font-weight: {FontType.buttonWeight}; "
                           f"border: 1px solid black;")

    """
        Установка визуального изменения курсора при наведения на кнопку.
    """
    def enterEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.ArrowCursor)