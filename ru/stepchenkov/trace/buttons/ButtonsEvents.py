from ru.stepchenkov.trace.types import TextType
from ru.stepchenkov.trace.types import ColorType


def down(self):
    self.direction.setText('↓')
    self.button_layout.addWidget(self.direction, 2, 1)


def left(self):
    self.direction.setText('←')
    self.button_layout.addWidget(self.direction, 1, 0)


def up(self):
    self.direction.setText('↑')
    self.button_layout.addWidget(self.direction, 0, 1)


def right(self):
    self.direction.setText('→')
    self.button_layout.addWidget(self.direction, 1, 2)


def obstacle(self):
    self.status = TextType.obstacle
    self.parent().set_obstacle(self)
    self.set_style(ColorType.obstacleGrey)


def start(self):
    self.status = TextType.start
    self.parent().set_start(self)
    self.weight_t.setText("Start")


def finish(self):
    self.status = TextType.finish
    self.parent().set_finish(self)
    self.weight_t.setText("End")
