from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QMessageBox

from ru.stepchenkov.trace.buttons.ButtonSetting import MenuButton
from ru.stepchenkov.trace.buttons.ButtonController import TraceButton
from ru.stepchenkov.trace.types import ColorType
from ru.stepchenkov.trace.types import TextType

if TYPE_CHECKING:
    from ru.stepchenkov.trace.window.MainWindow import MainWindow


class MainWindowInit(QWidget):

    def __init__(self, parent: 'MainWindow') -> None:
        super().__init__(parent)

        '''
            Создание переменных.
            1) Счетчик ячеек.
            2) Список свободных ячеек.
            3-4) Размеры сетки
        '''
        self.counter = 1
        self.cell = []
        self.weight: int = 10
        self.height: int = 10

        """
            1) Режимы start|end|obstacle.
            2) start.
            3) end.
            4) Текущая ячейка.
            5) Выход из алгоритма.
        """
        self.mode: Optional[str] = None
        self.start: Optional[TraceButton] = None
        self.finish: Optional[TraceButton] = None
        self.actual_cell: Optional[TraceButton] = None
        self.quit = False

        """
            Горизонтальная панель
        """
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        """
            Компановка сетки с ячейками.
        """
        self.trace_layout = QGridLayout()
        self.trace_layout.setAlignment(Qt.AlignLeft)
        self.trace_layout.setSpacing(0)

        """
            Компановка панели с кнопками.
        """
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setContentsMargins(0, 15, 0, 0)
        self.menu_layout.setAlignment(Qt.AlignTop)

        """
            Добавление обеих панелей на сцену.
        """
        self.layout.addLayout(self.menu_layout)
        self.layout.addLayout(self.trace_layout)

        """
            Вызов заполения.
        """
        self.fillingCells()

        """
            Создание кнопок и передача им парметров.
        """
        self.startButton = MenuButton(self, 'Поставить start')
        self.startButton.clicked.connect(lambda *args, mode=TextType.start: self.change_mode(mode))

        self.finishButton = MenuButton(self, 'Поставить finish')
        self.finishButton.clicked.connect(lambda *args, mode=TextType.finish: self.change_mode(mode))

        self.obstacleButton = MenuButton(self, 'Поставить преграду')
        self.obstacleButton.clicked.connect(lambda *args, mode=TextType.obstacle: self.change_mode(mode))

        """
            Добавление кнопок на сцену.
        """
        self.menu_layout.addWidget(self.startButton)
        self.menu_layout.addWidget(self.finishButton)
        self.menu_layout.addWidget(self.obstacleButton)

        """
            Вертикальная панель с кнопкой дальше.
        """
        self.done_layout = QVBoxLayout()
        self.menu_layout.addLayout(self.done_layout)
        self.done = MenuButton(self, "Дальше")

        """
            Обработка кнопки дальше и добавление на сцену.
        """
        self.done.clicked.connect(lambda: self.finish_preparation())
        self.done_layout.setAlignment(Qt.AlignBottom)
        self.done_layout.addWidget(self.done)

    """
        Добавление на сетку по координатам.
    """

    def fillingCells(self) -> None:
        for row in range(self.height):
            for column in range(self.weight):
                button = TraceButton(self, (row, column))
                self.trace_layout.addWidget(button, row, column)

    """
        Изменения режима.
    """
    def change_mode(self, mode: str):
        self.mode = mode

    """
        Установка в start.
    """
    def set_start(self, start: TraceButton) -> None:
        if self.start is not None:
            self.start.reset()
        if start == self.finish:
            self.finish = None
        self.start = start

    """
        Установка в finish.
    """
    def set_finish(self, finish: TraceButton) -> None:
        if self.finish is not None:
            self.finish.reset()
        if finish == self.start:
            self.start = None
        self.finish = finish

    """
        Установка в obstacle.
    """
    def set_obstacle(self, obstacle: TraceButton) -> None:
        if self.start == obstacle:
            self.start = None
        elif self.finish == obstacle:
            self.finish = None

    def finish_preparation(self) -> None:
        if self.start is None or self.finish is None:
            error = QMessageBox(self)
            error.setWindowTitle("Error")
            error.setText("Введите start or End")
            error.setStyleSheet(f"background-color: {ColorType.white};")
            error.setIcon(QMessageBox.Critical)
            error.show()
        else:
            self.startButton.disconnect()
            self.finishButton.disconnect()
            self.obstacleButton.disconnect()
            self.actual_cell = self.start
            self.mode = None

            """
                Изменения текста на кнопках и добавление новых функций
            """
            self.startButton.setText(TextType.create)
            self.startButton.clicked.connect(lambda: self.createPaths())

            self.finishButton.setText(TextType.cancel)
            self.finishButton.clicked.connect(lambda: self.parent().main_init())

            """
                Удалить кнопку obstacle.
            """
            self.obstacleButton.deleteLater()

            self.done.deleteLater()
            self.done_layout.deleteLater()

            """
                обновить слой.
            """
            self.trace_layout.update()

    """
        построение пути.
    """
    def createPaths(self) -> None:
        while True:
            self.step()
            if self.quit:
                break

    """
        берутся координаты текущей ячейки, на основе этих координат проверяются
        в порядке up -> right -> down -> left вокруг текущей ячейки, 
        если какая-то не рассмотрена и  не является преградой или концом,
        то записываем вес, заполняем все остальное, и добавляем в качестве доступной,
        если же для текущей ячейки все ячейки вокруг просмотрены,
        то достаем первую из списка доступных.
    """
    def step(self) -> None:
        row = self.actual_cell.coordinates[0]
        column = self.actual_cell.coordinates[1]

        status = False
        direction = ""
        if row > 0 and TextType.up not in self.actual_cell.paths:
            status = True
            row -= 1
            direction = TextType.up
            self.actual_cell.paths.append(TextType.up)
        elif column < self.weight - 1 and TextType.right not in self.actual_cell.paths:
            status = True
            column += 1
            direction = TextType.right
            self.actual_cell.paths.append(TextType.right)
        elif row < self.height - 1 and TextType.down not in self.actual_cell.paths:
            status = True
            row += 1
            direction = TextType.down
            self.actual_cell.paths.append(TextType.down)
        elif column > 0 and TextType.left not in self.actual_cell.paths:
            status = True
            column -= 1
            direction = TextType.left
            self.actual_cell.paths.append(TextType.left)
        if status:
            cell_ind = self.trace_layout.itemAtPosition(row, column).widget()
            if cell_ind.status is None:
                weight = self.actual_cell.weight + 1
                cell_ind.set_info(self.counter, weight, direction)
                cell_ind.status = "fail"
                cell_ind.parent_cell = self.actual_cell
                self.counter += 1
                self.cell.append(cell_ind)
            elif cell_ind.status == TextType.finish:
                cell_ind.set_direction(direction)
                self.finishButton.setEnabled(False)
                self.startButton.setEnabled(False)
                self.coloring()
                self.quit = True
            else:
                self.step()
        else:
            self.actual_cell = self.cell[0]
            self.cell.remove(self.actual_cell)
            self.step()

    """
        Окрашивание конечного пути
    """

    def coloring(self) -> None:
        while self.actual_cell.parent_cell is not None:
            self.actual_cell.set_style(ColorType.yellow)
            self.actual_cell = self.actual_cell.parent_cell
        self.start.set_style(ColorType.yellow)
        self.finish.set_style(ColorType.yellow)
