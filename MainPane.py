from PyQt5.QtWidgets import *
from GameManager import *


class TetMainPane(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(520, 770)
        self.setWindowTitle("Mr. Tetris")
        self.__manager = GameManager(self)
