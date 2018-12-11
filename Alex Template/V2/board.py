from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location

    # todo set the board with and height in square
    boardWidth  = 0     # board is 0 square wide - this needs updating
    boardHeight = 0     #
    timerSpeed  = 1000  # the timer updates ever 1 second
    counter     = 10    # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started
        self.start()                # start the game which will start the timer

        self.boardArray             # Todo - create a 2d int/Piece array to story the state of the game
        # self.printBoardArray()    # Todo - uncomment this method after create the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / Board.boardWidth

    def squareHeight(self):
        '''returns the height of one squarein the board'''
        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # boolean which determines if the game has started or not is true
        self.resetGame()                            # reset the game
        self.timer.start(Board.timerSpeed, self)    # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # todo adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            Board.counter = Board.counter - 1
            print('timerEvent()', Board.counter)
            self.updateTimerSignal.emit(Board.counter)
        else:
            super(Board, self).timerEvent(event)  # other wise pass it to the super class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        # painter = QPainter(self)
        # self.drawBoardSquares(painter)
        # self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.x())+","+str(event.y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        # todo you could call some game lodic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # todo write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # todo set the dafault colour of the brush
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth()* col # Todo set this value equal the transformation you would like in the column direction
                rowTransformation = 0  # Todo set this value equal the transformation you would like in the column direction
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect() # Todo provide the required arguements
                painter.restore()
                # todo change the colour of the brush so that a checkered board is drawn

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.transparent
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate()
                #Todo choose your colour and set the painter brush to the correct colour

                # Todo draw some the pieces as elipses
                radius = (self.squareWidth() - 2) / 2  # Todo - make a radius in the y direction too
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
