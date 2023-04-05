from typing import TYPE_CHECKING

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout

from ru.stepchenkov.trace.types import ColorType as Color
from ru.stepchenkov.trace.types import FontType as Font
from ru.stepchenkov.trace.buttons import ButtonsEvents
from ru.stepchenkov.trace.types import TextType
from ru.stepchenkov.trace.types import ColorType

if TYPE_CHECKING:
    from ru.stepchenkov.trace.window.MainWindow import MainWindowInit


class TraceButton(QPushButton):

    def __init__(self, parent: 'MainWindowInit', coordinates: tuple[int, int]) -> None:
        super().__init__(parent)

        """
            Параметры ячейки.
        """
        self.setFixedSize(Font.cellSize, Font.cellSize)
        self.coordinates = coordinates
        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(0)
        self.button_layout.setAlignment(Qt.AlignCenter)

        """
            Установка изначальных значений.
        """
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setColumnMinimumWidth(0, 8)
        self.button_layout.setColumnMinimumWidth(1, 8)
        self.button_layout.setColumnMinimumWidth(2, 8)
        self.button_layout.setRowMinimumHeight(0, 8)
        self.button_layout.setRowMinimumHeight(1, 8)
        self.button_layout.setRowMinimumHeight(2, 8)
        self.setLayout(self.button_layout)

        """
            1) Статус.
            2) Номер ячейки.
            3) Направление.
            4) Вес
            5) Родительская ячейка
        """
        self.status = None
        self.order = None
        self.paths = []
        self.weight = 0
        self.parent_cell = None

        '''
            Настройка текста внутри ячееек 
            -> выравнивание, шрифт, расположение.
            
            -> цвет фона в сетке.
        '''
        self.order_t = QLabel(self)
        self.order_t.setAlignment(Qt.AlignCenter)
        self.order_t.setFont(QFont(Font.fontArial, Font.fontSize))
        self.button_layout.addWidget(self.order_t, 0, 2)

        self.weight_t = QLabel(self)
        self.weight_t.setAlignment(Qt.AlignCenter)
        self.weight_t.setFont(QFont(Font.fontArial, Font.fontSize))
        self.button_layout.addWidget(self.weight_t, 1, 1)

        self.direction = QLabel(self)
        self.direction.setAlignment(Qt.AlignCenter)
        self.direction.setFont(QFont(Font.fontArial, Font.fontSize))
        self.direction.setVisible(False)

        self.set_style(Color.black)

    """
        Стиль ячеек.
    """

    def set_style(self, color: str):
        self.setStyleSheet(f'background-color: #{color}; border: 1px solid black;')
        self.order_t.setStyleSheet('border: none;')
        self.weight_t.setStyleSheet('border: none;')
        self.direction.setStyleSheet('border: none;')

    """
        Визуальные изменения при наведении на сетку.
    """
    def enterEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.ArrowCursor)

    """
        Кнопка сброса.
    """
    def reset(self):
        self.status = None
        self.set_style(ColorType.black)
        self.weight_t.setText("")

    """
        Устанавливаем в ячейку информацию.
    """
    def set_info(self, order: int, weight: int, direction: str):
        self.order = order
        self.order_t.setText(str(order))
        self.weight = weight
        self.weight_t.setText(str(weight))
        self.set_direction(direction)

    """
        Добавляем в ячейку стрелочку.
    """
    def set_direction(self, direction: str):
        if direction == TextType.up:
            ButtonsEvents.down(self)
        elif direction == TextType.right:
            ButtonsEvents.left(self)
        elif direction == TextType.down:
            ButtonsEvents.up(self)
        elif direction == TextType.left:
            ButtonsEvents.right(self)
        self.direction.setVisible(True)

    """
        Обработка нажатия на кнопки.
    """
    def mousePressEvent(self, event: QEvent) -> None:
        if self.parent().mode is not None:
            self.reset()
            if event.button() == Qt.LeftButton and self.parent().mode == TextType.obstacle:
                ButtonsEvents.obstacle(self)
            elif event.button() == Qt.LeftButton and self.parent().mode == TextType.start:
                ButtonsEvents.start(self)
            elif event.button() == Qt.LeftButton and self.parent().mode == TextType.finish:
                ButtonsEvents.finish(self)