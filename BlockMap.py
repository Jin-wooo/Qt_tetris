from PyQt5.QtWidgets import QFrame
from Block import *


class BlockMap(QFrame):
    def __init__(self, parent):
        super(BlockMap, self).__init__(parent)
        self._maxMapWidth = 10  # 테트리스 맵의 넓이
        self._maxHNumBlock = 10  # 맵 가로에 들어가는 최대 블럭 갯수
        self._maxVNumBlock = 22  # 세로에 들어가는 최대 블럭 갯수
        self._maxMapHeight = 22  # 테트리스 맵의 높이
        self._mapWhiteSpace = 10

        # 테트리스 맵 프레임 & 세팅
        self.setGeometry(10, 10, 342, 750)
        # self.resize(341, 749)
        # self.move(self._mapWhiteSpace, self._mapWhiteSpace)
        # self.setEnabled(True)
        self.setFrameShape(QFrame.Box)

        # 테트리스 맵의 블럭 위치를 기록하는 배열
        self.__mapBlock = []

        # 맵의 각 끝지점 좌표 저장
        self.__numMapTop = self.rect().top() + self._mapWhiteSpace
        self.__numMapBottom = self.rect().bottom() + self._mapWhiteSpace
        self.__numMapLeft = self.rect().left() + self._mapWhiteSpace
        self.__numMapRight = self.rect().right() + self._mapWhiteSpace

        # 맵 왼쪽 꼭대기 좌표는 늘 쓰이므로 저장
        self.__blockSize = self.__numMapLeft / self._maxMapWidth

    def getMapBlock(self, _x, _y):
        return self.__mapBlock[_y][_x]

    def setMapBlock(self, _x, _y, _val):
        self.__mapBlock[_y][_x] = _val

    def getMapWidth(self):
        return self._maxMapWidth

    def getMapHeight(self):
        return self._maxMapHeight

    def getMapTop(self):
        return self.__numMapTop

    def getMapBottom(self):
        return self.__numMapBottom

    def getMapRight(self):
        return self.__numMapRight

    def getMapLeft(self):
        return self.__numMapLeft

    def getWhiteSpace(self):
        return self._mapWhiteSpace

    def isLineFilled(self, _idx):
        return 0 not in self.__mapBlock[_idx]

    def clearLine(self, _idx):
        self.__mapBlock.remove(self.__mapBlock[_idx])
        self.__mapBlock.insert(0, [Tetromino.No_Shape] * self._maxMapWidth)

    def clearMap(self):
        self.__mapBlock.clear()
        for i in range(self._maxMapHeight):
            tmpList = []
            for j in range(self._maxMapWidth):
                tmpList.append(0)
            self.__mapBlock.append(tmpList)


    """
    def paintEvent(self, event):
        rect = self.__paneMap.contentsRect()
        print(rect.top())
        print(rect.width())

        qp = QPainter(self)
        pen = QPen(Qt.gray)
        qp.setPen(pen)
        qp.begin(self)

        # 라인을 그리는 함수
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

        # 2. 지금 현재 블럭 색칠하기
        if self._playBlock.getShape() != Block.Tetromino.No_Shape:
            for iterBlk in range(self._playBlock.getBlockSize()):
                ptTmpX = self._curX + self._playBlock.getX(iterBlk)
                ptTmpY = self._curY + self._playBlock.getY(iterBlk)
                self.drawBlock(qp, ptTmpX, ptTmpY,
                               self._playBlock.getShape())
        qp.end()
    """




 # 색칠 테스트용
    """
       for iterY in range(0, self.__paneMap.getMapHeight()):
            for iterX in range(0, self.__paneMap.getMapWidth()):
                self.drawBlock(qp, iterX, iterY,
                               self.__paneMap.getMapBlock(iterX, iterY))
        self.drawBlock(qp, 3, 2, 7)
    """