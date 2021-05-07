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
        self._nextBlock = Block.TetBlock()        # 다음 블럭 생성
        self._nextBlock.setRandomShape()
        self._playBlock.randomRotate()  # 현재 블럭 쏠 준비

        self.__paneNext.showNextBlock(self._nextBlock.getShape())
        # randX = random.randint(1, self.__paneMap.getMapWidth() - 2)

        if not self.tryMove(self._playBlock, 5, 1):  # Y는 최소 -1
            self.gameOver()

    def linedownBlock(self):
        if not self.tryMove(self._playBlock, self._curX, self._curY + 1):
            self.droppedBlock()

    def droppedBlock(self):
        # 블럭의 현 위치를 맵에 기록
        for iterDrop in range(self._playBlock.getBlockSize()):
            dropX = self._curX + self._playBlock.getX(iterDrop)
            dropY = self._curY + self._playBlock.getY(iterDrop)

            self.__paneMap.setMapBlock(dropX, dropY,
                                       self._playBlock.getShape())
        # 다 찬 라인 날리기
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
        # 블럭 내 모든 좌표를 검사한다.
        for iterMv in range(newBlock.getBlockSize()):
            # 임시좌표 = 새 좌표 + 블럭기준 좌표 = 블럭좌표를 맵에 대입
            tmpX = newX + newBlock.getX(iterMv)
            tmpY = newY + newBlock.getY(iterMv)

            # 맵 밖으로 나갔는가?
            if not 0 <= tmpX < self.__paneMap.getMapWidth():
                return False
            if not 0 <= tmpY < self.__paneMap.getMapHeight():
                return False

            # 그 방향으로 가면 걸리는가?
            if self.__paneMap.getMapBlock(tmpX, tmpY) \
                    != Block.Tetromino.No_Shape:
                return False

        # 다 통과했으면, 블럭의 현재 좌표를 바꿔준다.
        self._playBlock = newBlock
        self._curX = newX
        self._curY = newY
        self.update()

        return True

    def drawBlock(self, painter, _x, _y, blockType):
        # 각 블럭 칸을 색칠해주는 착한 함수.
        # 값이 조금이라도 틀어지면 골치아파짐. 수정 X
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


        # 맵 격자
        for i in range(1, self.__paneMap.getMapHeight()):
            paintY = i * self.oneBlockSize + self._mapWSpace
            qp.drawLine(self.__paneMap.getMapLeft(), paintY,
                        self.__paneMap.getMapRight(), paintY)
        for j in range(1, self.__paneMap.getMapWidth()):
            paintX = j * self.oneBlockSize + self._mapWSpace
            qp.drawLine(paintX, self.__paneMap.getMapTop(),
                        paintX, self.__paneMap.getMapBottom())

        # 페인트 이벤트의 핵심
        # 1. 맵에 있는 모든 블럭을 색칠하기
        for iterY in range(0, self.__paneMap.getMapHeight()):
            for iterX in range(0, self.__paneMap.getMapWidth()):
                tmpBlock = self.getBlock(iterX, iterY)
                if tmpBlock != Block.Tetromino.No_Shape:
                    self.drawBlock(qp, iterX, iterY, tmpBlock)

        # 2. 현재 컨트롤하는 블럭 색칠하기
        if self._playBlock.getShape() != Block.Tetromino.No_Shape:
            for iterBlk in range(self._playBlock.getBlockSize()):
                ptTmpX = self._curX + self._playBlock.getX(iterBlk)
                ptTmpY = self._curY + self._playBlock.getY(iterBlk)
                self.drawBlock(qp, ptTmpX, ptTmpY,
                               self._playBlock.getShape())

        # 게임 오버 연출화면
        if not self._isGameStarted:
            overCol = QColor(150, 150, 150, 160)
            qp.fillRect(self.__paneMap.getMapLeft(),
                        self.__paneMap.getMapTop(),
                        self.__paneMap.getMapRight() - 10,
                        self.__paneMap.getMapBottom() - 10,
                        overCol)
            qp.setPen(Qt.black)
            qp.setFont(QFont('나눔명조', 40))
            qp.drawText(12, 405,"GAME OVER")
            print("GAME OVER")
            return

        qp.end()

    def timerEvent(self, a0: QTimerEvent) -> None:
        """Controls block drop"""
        # 라인 제거가 끝나면 새 블럭을 만들어줘야함
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
