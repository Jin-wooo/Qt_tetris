from random import randint


class Tetromino(object):
    No_Shape = 0
    Z_Shape = 1
    S_Shape = 2
    L_Shape = 3
    J_Shape = 4
    Square_Shape = 5
    T_Shape = 6
    Line_Shape = 7


class TetBlock(object):
    cm_blockData = \
        (
            ((0, 0),(0, 0),(0, 0),(0, 0)),          # No_Shape
            ((0 ,-1), (0, 0), (-1, 0), (-1, 1)),    # □■□
                                                    # ■■□
                                                    # ■□□

            ((0, -1), (0, 0), (1, 0), (1, 1)),      # □■□
                                                    # □■■
                                                    # □□■

            ((0, -1), (0, 0), (0, 1), (1, 1)),      # □■□
                                                    # □■□
                                                    # □■■

            ((0, -1), (0, 0), (0, 1), (-1, 1)),     # □■□
                                                    # □■□
                                                    # ■■□

            ((0, 0), (1, 0), (0, 1), (1, 1)),       # □□□
                                                    # □■■
                                                    # □■■

            ((0, -1), (-1, 0), (0, 0), (1, 0)),     # □■□
                                                    # ■■■
                                                    # □□□

            ((0, -1), (0, 0), (0, 1), (0, 2))       # □■□□
                                                    # □■□□
                                                    # □■□□
                                                    # □■□□
        )

    def __init__(self, blocksize = 4):
        self.__blockSize = blocksize
        self.__blockData = [[0, 0] for i in range(self.__blockSize)]

        if blocksize == 4:
            self.__blockShape = Tetromino.No_Shape
        elif blocksize == 5:
            pass

    def setShapeData(self, shapeIdx):
        """sets all of TetBlock"""
        self.setShape(shapeIdx)
        shapetype = self.cm_blockData[shapeIdx]
        for iterShape in range(self.__blockSize):
            self.__blockData[iterShape][0] = shapetype[iterShape][0]
            self.__blockData[iterShape][1] = shapetype[iterShape][1]

    def setShape(self, shapeIdx):
        """sets just a shpae, not a shape data"""
        self.__blockShape = shapeIdx

    def setRandomShape(self):
        self.setShapeData(randint(1, 7))

    def getShape(self):
        return self.__blockShape

    def getBlockSize(self):
        return self.__blockSize

    def setX(self, _idx, _x):
        self.__blockData[_idx][0] = _x

    def setY(self, _idx, _y):
        self.__blockData[_idx][1] = _y

    def getX(self, _idx):
        return self.__blockData[_idx][0]

    def getY(self, _idx):
        return self.__blockData[_idx][1]

    def topPoint(self):
        """
        Lowest value of Y
        :return: top index of map
        """
        numTop = 10
        for i in range(0, self.__blockSize):
            if self.__blockData[i][1] > numTop:
                numTop = self.__blockData[i][1]
        return numTop

    def bottomPoint(self):
        """Highest value of Y"""
        numBottom = -10
        for i in range(0, self.__blockSize):
            if self.__blockData[i][1] < numBottom:
                numBottom = self.__blockData[i][1]
        return numBottom

    def leftPoint(self):
        """Lowest Value of X"""
        numLeft = 10
        for  i in range(0, self.__blockSize):
            if self.__blockData[i][0] > numLeft:
                numLeft = self.__blockData[i][1]
        return numLeft

    def rightPoint(self):
        """Highest Value of X"""
        numRight = -10
        for i in range(0, self.__blockSize):
            if self.__blockData[i][0] < numRight:
                numRight = self.__blockData[i][1]
        return numRight

    def rotateLeft(self):
        # 네모 모양이면 굳이 안돌려도 되니까 그냥 리턴
        if self.__blockShape == Tetromino.Square_Shape:
            return self

        # 임시 블럭을 받았던 블럭에 맞게 세팅
        tmpShape = TetBlock()
        tmpShape.setShapeData(self.getShape())

        # 블럭 좌표 이동
        for iterRotate in range(self.__blockSize):
            tmpShape.setX(iterRotate, self.getY(iterRotate))
            tmpShape.setY(iterRotate, -(self.getX(iterRotate)))

        return tmpShape

    def rotateRight(self):
        # 네모 모양이면 굳이 안돌려도 되니까 그냥 리턴
        if self.__blockShape == Tetromino.Square_Shape:
            return self

        # 임시 블럭을 받았던 블럭에 맞게 세팅
        tmpShape = TetBlock()
        tmpShape.setShapeData(self.getShape())

        # 블럭 좌표 이동
        for iterRotate in range(self.__blockSize):
            tmpShape.setX(iterRotate, -(self.getY(iterRotate)))
            tmpShape.setY(iterRotate, self.getX(iterRotate))

        return tmpShape

    def randomRotate(self):
        """
        Randomly rotate block for newBlock
        :return: Rotated Shape
        """
        numRand = randint(0, 3)     # X 0 X
        if numRand == 0:            # 3   1
            return self             # X 2 X

        tmpShape = TetBlock()
        tmpShape.setShapeData(self.getShape())
        for iterRotate in range(self.__blockSize):
            if numRand == 1:
                tmpShape.setX(iterRotate, -(self.getY(iterRotate)))
                tmpShape.setY(iterRotate, self.getX(iterRotate))
            elif numRand == 3:
                tmpShape.setX(iterRotate, self.getY(iterRotate))
                tmpShape.setY(iterRotate, -(self.getX(iterRotate)))
            else:
                tmpShape.setX(iterRotate, self.getX(iterRotate))
                tmpShape.setY(iterRotate, -(self.getY(iterRotate)))

        return tmpShape
