from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import Block
import blockIMG


class NextBlockPane(QGroupBox):
    def __init__(self, parent):
        super(NextBlockPane, self).__init__(parent)
        self.__nextLabel = QLabel(self)

        self.initUI()

    def initUI(self):
        # NextBlockPane 기본세팅
        self.setGeometry(370, 20, 130, 120)
        self.setTitle("NEXT")
        self.setAlignment(Qt.AlignCenter)

    def showNextBlock(self, _type):

        if _type == Block.Tetromino.Square_Shape:
            self.__nextLabel.setGeometry(2, 6, 112, 112)
            TetIMG = QPixmap(":/IMG/5.png").scaledToWidth(128)

        elif _type == Block.Tetromino.T_Shape:
            self.__nextLabel.setGeometry(2, 5, 112, 112)
            TetIMG = QPixmap(":/IMG/6.png").scaledToWidth(128)

        elif _type == Block.Tetromino.Line_Shape:
            self.__nextLabel.setGeometry(15, 7, 112, 112)
            TetIMG = QPixmap(":/IMG/7.png").scaledToWidth(102)

        elif 1 <=_type <= 4:
            self.__nextLabel.setGeometry(2, 7, 112, 112)
            #tmpStr = str(_type) + "a"
            TetIMG = \
                QPixmap(":/IMG/" + str(_type) + ".png").scaledToWidth(128)
        else:
            return
        self.__nextLabel.setPixmap(TetIMG)

class ScorePane(QGroupBox):
    def __init__(self, parent):
        super(ScorePane, self).__init__(parent)

        # 점수 기록용 LCD 패널
        self.__lcdNum = QLCDNumber(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(370, 160, 130, 60)
        self.setTitle("SCORE")
        self.setAlignment(Qt.AlignCenter)

        self.__lcdNum.setGeometry(10, 10, 110, 50)
        self.__lcdNum.setSegmentStyle(QLCDNumber.Filled)
        self.__lcdNum.setFrameShape(QFrame.NoFrame)

    def addScore(self, _score):
        self.__lcdNum.display(_score)



