from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter

from piece import Piece
from player import Player

class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    boardWidth = 8
    boardHeight = 8
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        # self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()
        
        self.currentPlayer = Player.Player1
        self.currentPlayer = 1

        self.boardArray = [
			[0, 1, 0, 1, 0, 1, 0, 1]
			[1, 0, 1, 0, 1, 0, 1, 0]
			[0, 1, 0, 1, 0, 1, 0, 1]
			[0, 0, 0, 0, 0, 0, 0, 0]
			[0, 0, 0, 0, 0, 0, 0, 0]
			[2, 0, 2, 0, 2, 0, 2, 0]
			[0, 2, 0, 2, 0, 2, 0, 2]
			[2, 0, 2, 0, 2, 0, 2, 0]
		]
        self.printBoardArray()


    def printBoardArray(self):
        '''prints the boardArray in an arractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        xMouseEvent = event.x()
        yMouseEvent = event.y()
        squareHeight = self.squareHeight()
        squareWidth = self.squareWidth()
        row = int(yMouseEvent/squareHeight)
        col = int(xMouseEvent/squareWidth)

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / Board.boardWidth

    def squareHeight(self):
        '''returns the height of one squarein the board'''
        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        '''starts game'''
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.msg2Statusbar.emit(str("status message"))

        self.timer.start(Board.Speed, self)

    def pause(self):
        '''pauses game'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str("status message"))
        self.update()

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        rect = self.contentRect()
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        print("click location [", event.x(), ",", event.y(), "]")
        self.mousePosToColRow(event)

    def keyPressEvent(self, event):
        '''processes key press events if you would like to do any'''
        if not self.isStarted or self.curPiece.shape() == Piece.NoPiece:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        '''handles timer event'''
        #todo adapter this code to handle your timers

        if event.timerId() == self.timer.timerId():
            pass
        else:
            super(Board, self).timerEvent(event)

    def resetGame(self):
        '''clears pieces from the board'''
        # todo write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawGrid(self, painter):
        '''draw all the square on the board'''
        # todo set the dafault colour of the brush
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                if (row + col) % 2 == 0:
				    colour = Qt.white
				else:
				    colour = Qt.black
				painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())
                painter.setBrush(colour)
                painter.fillRect(0, 0, )
                painter.restore()

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.transparent
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate()
                if colorAsInt == 0:
				    colour = Qt.transparent
				elif colorAsInt == 1:
				    colour = Qt.red
				elif colorAsInt == 2:
				    colour = Qt.blue
				painter.setbrush(colour)
                if colorAsInt > 0:
                    radius = (self.squareWidth() - 2) / 2
                    center = QPoint(radius, radius)
                    painter.drawEllipse(center, radius, radius)
                painter.restore()
