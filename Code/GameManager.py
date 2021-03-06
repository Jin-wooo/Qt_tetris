import random
from PyQt5.QtCore import Qt, QBasicTimer, QTimerEvent
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont, QColor, QPainter
import Panes
import Block
import BlockMap


class GameManager(QWidget):
    c_blockColor = [0x000000, 0xE13A5F, 0xEA7C4E, 0xF6D34A,
                    0x82AA28, 0x45A1DE, 0x445CBB, 0x9E4491]

    def __init__(self, parent):
        super(GameManager, self).__init__(parent)
        self.resize(parent.size())
        self.__paneMap = BlockMap.BlockMap(self)
        self.__paneNext = Panes.NextBlockPane(self)
        self.__paneScore = Panes.ScorePane(self)

        self.__timer = QBasicTimer()
        self._playBlock = Block.TetBlock()
        self._nextBlock = Block.TetBlock()
        self._curX = 0
        self._curY = 0
        self._isGameStarted = False
        self._isGamePaused = False
        self._bAfterClearLine = False
        self._numGameSpeed = 300
        self.oneBlockSize = int(self.__paneMap.width()\
                            / self.__paneMap.getMapWidth())
        self._mapWSpace = self.__paneMap.getWhiteSpace()
        self._blockSpace = 1
        self._numRemovedLine = 0

        self.setFocusPolicy(Qt.StrongFocus)
        self.startGame()

    def getBlock(self, _x, _y):
        return self.__paneMap.getMapBlock(_x, _y)

    def startGame(self):
        """starts game"""
        if self._isGamePaused:
            return

        self._isGameStarted = True
        self._bAfterClearLine = False
        self.__paneMap.clearMap()
        self._numRemovedLine = 0

        self._nextBlock.setRandomShape()
        self.newBlock()

        self.__timer.start(self._numGameSpeed, self)

    def pause(self):
        if not self._isGameStarted:
            return
        self._isGamePaused = not self._isGamePaused

        if self._isGamePaused:
            self.__timer.stop()
        else:
            self.__timer.start(self._numGameSpeed, self)

    def newBlock(self):
        self._playBlock = self._nextBlock
        self._nextBlock = Block.TetBlock()        # ?????? ?????? ??????
        self._nextBlock.setRandomShape()
        self._playBlock.randomRotate()  # ?????? ?????? ??? ??????

        self.__paneNext.showNextBlock(self._nextBlock.getShape())
        # randX = random.randint(1, self.__paneMap.getMapWidth() - 2)

        if not self.tryMove(self._playBlock, 5, 1):  # Y??? ?????? -1
            self.gameOver()

    def linedownBlock(self):
        if not self.tryMove(self._playBlock, self._curX, self._curY + 1):
            self.droppedBlock()

    def droppedBlock(self):
        # ????????? ??? ????????? ?????? ??????
        for iterDrop in range(self._playBlock.getBlockSize()):
            dropX = self._curX + self._playBlock.getX(iterDrop)
            dropY = self._curY + self._playBlock.getY(iterDrop)

            self.__paneMap.setMapBlock(dropX, dropY,
                                       self._playBlock.getShape())
        # ??? ??? ?????? ?????????
        self.clearMapLine()

        if not self._bAfterClearLine:
            self.newBlock()

    def FallDownBlock(self):
        fallY = self._curY
        while fallY > 0:
            if not self.tryMove(self._playBlock, self._curX, fallY + 1):
                break
            fallY += 1

        self.droppedBlock()

    def clearMapLine(self):
        for iterClr in range(self.__paneMap.getMapHeight()):
            if self.__paneMap.isLineFilled(iterClr):
                self.__paneMap.clearLine(iterClr)
                self._numRemovedLine += 10

        self._bAfterClearLine = True
        self.__paneScore.addScore(self._numRemovedLine)

    def tryMove(self, newBlock, newX, newY):
        # ?????? ??? ?????? ????????? ????????????.
        for iterMv in range(newBlock.getBlockSize()):
            # ???????????? = ??? ?????? + ???????????? ?????? = ??????????????? ?????? ??????
            tmpX = newX + newBlock.getX(iterMv)
            tmpY = newY + newBlock.getY(iterMv)

            # ??? ????????? ?????????????
            if not 0 <= tmpX < self.__paneMap.getMapWidth():
                return False
            if not 0 <= tmpY < self.__paneMap.getMapHeight():
                return False

            # ??? ???????????? ?????? ?????????????
            if self.__paneMap.getMapBlock(tmpX, tmpY) \
                    != Block.Tetromino.No_Shape:
                return False

        # ??? ???????????????, ????????? ?????? ????????? ????????????.
        self._playBlock = newBlock
        self._curX = newX
        self._curY = newY
        self.update()

        return True

    def drawBlock(self, painter, _x, _y, blockType):
        # ??? ?????? ?????? ??????????????? ?????? ??????.
        # ?????? ??????????????? ???????????? ???????????????. ?????? X
        drawX = _x * self.oneBlockSize + self._blockSpace + 11
        drawY = _y * self.oneBlockSize + self._blockSpace + 11
        painter.fillRect(drawX, drawY,
                         self.oneBlockSize - 3,
                         self.oneBlockSize - 3,
                         QColor(Qt.black))

        drawX = drawX + 2
        drawY = drawY + 2
        painter.fillRect(drawX, drawY,
                         self.oneBlockSize - 7,
                         self.oneBlockSize - 7,
                         QColor(self.c_blockColor[blockType]))

    def paintEvent(self, event):
        qp = QPainter(self)
        col = Qt.gray
        qp.setPen(col)
        qp.begin(self)


        # ??? ??????
        for i in range(1, self.__paneMap.getMapHeight()):
            paintY = i * self.oneBlockSize + self._mapWSpace
            qp.drawLine(self.__paneMap.getMapLeft(), paintY,
                        self.__paneMap.getMapRight(), paintY)
        for j in range(1, self.__paneMap.getMapWidth()):
            paintX = j * self.oneBlockSize + self._mapWSpace
            qp.drawLine(paintX, self.__paneMap.getMapTop(),
                        paintX, self.__paneMap.getMapBottom())

        # ????????? ???????????? ??????
        # 1. ?????? ?????? ?????? ????????? ????????????
        for iterY in range(0, self.__paneMap.getMapHeight()):
            for iterX in range(0, self.__paneMap.getMapWidth()):
                tmpBlock = self.getBlock(iterX, iterY)
                if tmpBlock != Block.Tetromino.No_Shape:
                    self.drawBlock(qp, iterX, iterY, tmpBlock)

        # 2. ?????? ??????????????? ?????? ????????????
        if self._playBlock.getShape() != Block.Tetromino.No_Shape:
            for iterBlk in range(self._playBlock.getBlockSize()):
                ptTmpX = self._curX + self._playBlock.getX(iterBlk)
                ptTmpY = self._curY + self._playBlock.getY(iterBlk)
                self.drawBlock(qp, ptTmpX, ptTmpY,
                               self._playBlock.getShape())

        # ?????? ?????? ????????????
        if not self._isGameStarted:
            overCol = QColor(150, 150, 150, 160)
            qp.fillRect(self.__paneMap.getMapLeft(),
                        self.__paneMap.getMapTop(),
                        self.__paneMap.getMapRight() - 10,
                        self.__paneMap.getMapBottom() - 10,
                        overCol)
            qp.setPen(Qt.black)
            qp.setFont(QFont('????????????', 40))
            qp.drawText(12, 405,"GAME OVER")
            print("GAME OVER")
            return

        qp.end()

    def timerEvent(self, a0: QTimerEvent) -> None:
        """Controls block drop"""
        # ?????? ????????? ????????? ??? ????????? ??????????????????
        if self._bAfterClearLine:
            self._bAfterClearLine = False
            self.newBlock()
        else:
            self.linedownBlock()

    def keyPressEvent(self, event):
        if not self._isGameStarted or \
                self._playBlock.getShape() == Block.Tetromino.No_Shape:
            super(GameManager, self).keyPressEvent(event)
            return
            
        instKey = event.key()

        if instKey == Qt.Key_0:
            self.pause()
            return

        if instKey == Qt.Key_4:
            self.tryMove(self._playBlock, self._curX - 1, self._curY)
        elif instKey == Qt.Key_6:
            self.tryMove(self._playBlock, self._curX + 1, self._curY)
        elif instKey == Qt.Key_7:
            self.tryMove(self._playBlock.rotateLeft(),
                         self._curX, self._curY)
        elif instKey == Qt.Key_9:
            self.tryMove(self._playBlock.rotateRight(),
                         self._curX, self._curY)
        elif instKey == Qt.Key_8:
            self.FallDownBlock()
        else:
            super(GameManager, self).keyPressEvent(event)

    def gameOver(self):
        """It`s end game now..."""
        self.__timer.stop()
        self._isGameStarted = False
        self._playBlock.setShape(Block.Tetromino.No_Shape)
        self.update()
