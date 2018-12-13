from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame, QLabel
from piece import Piece
from player import Player


class Board(QFrame):
    msg2StatusBar = pyqtSignal(str)
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location

    boardWidth = 8
    boardHeight = 8
    Speed = 300
    timerSpeed  = 1000  # the timer updates ever 1 second
    counter = 10  # the number the counter will count down from


    def __init__(self, parent):
        super().__init__(parent)
        self.init_board()

    def init_board(self):
        # initiates board
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clear_board()
        self.start()                # start the game which will start the timer
        self.clicks = 0
        self.current_piece, self.current_pos, self.new_piece, self.new_pos = (), (), (), ()

        self.currentPlayer = Player.Player1

        self.boardArray = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
        ]
        self.print_board_array()

    def print_board_array(self):
        # prints the boardArray in an attractive way
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mouse_pos_to_col_row(self, event):
        # convert the mouse click event to a row and column
        self.click_row = int(event.y() / self.square_height())
        self.click_col = int(event.x() / self.square_width())
        # print(self.boardArray[self.click_row][self.click_col])
        print(int(event.x()), ", ", int(event.y()))
        # clickLoc = "click location: " + str(self.boardArray[self.click_row][self.click_col])
        # self.clickLocationSignal.emit(clickLoc)
        piece = self.boardArray[self.click_row][self.click_col]
        square = (self.click_row, self.click_col)
        print(piece, square)
        return piece, square

    def square_width(self):
        # returns the width of one square in the board
        return self.contentsRect().width() / Board.boardWidth

    def square_height(self):
        # returns the height of one square in the board
        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        # starts game
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clear_board()

        self.msg2StatusBar.emit(str("status message"))

        self.timer.start(Board.Speed, self)
        print("start () - timer is started")

    def pause(self):
        # pauses game

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2StatusBar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2StatusBar.emit(str("status message"))
        self.update()

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # todo adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            Board.counter = Board.counter - 1
            self.updateTimerSignal.emit(Board.counter)
        else:
            super(Board, self).timerEvent(event)  # other wise pass it to the super class for handling

    def paintEvent(self, event):
        # paints the board and the pieces of the game
        painter = QPainter(self)
        # rect = self.contentRect()
        self.draw_grid(painter)
        self.draw_pieces(painter)

    def mousePressEvent(self, event):
        if self.clicks == 0:
            self.clicks += 1
            print("1st click")
            self.current_piece, self.current_pos = self.mouse_pos_to_col_row(event)
        elif self.clicks == 1:
            self.clicks += 1
            print("2nd click")
            self.new_piece, self.new_pos = self.mouse_pos_to_col_row(event)
            self.boardArray[self.new_pos[0]][self.new_pos[1]] = self.boardArray[self.current_pos[0]][self.current_pos[1]]
            self.boardArray[self.current_pos[0]][self.current_pos[1]] = 0
        print(self.clicks)
        self.update()
        print("update?")
        # self.clicks = 0


        # if event.button() == Qt.LeftButton:

        '''
        returns a QPoint with a tuple (x, y) col, row

        call a "game logic" function to determine:

        if 1st click:  #select piece
            if isEmpty or opponent piece:
                break
            selectPiece()
            highlightMoveOptions() #show permitted spaces to move to
                if noOptions:
                    break
        if 2nd click: # select square to put piece selected in 1st click
            if isNotEmpty:
                break
            movePiece()
            removeCapturedPiece()
            if pieceRemoved():
                removeCapturedPiece()
                updateScoreBoard()
                didIWin()
        '''

    # def getPieces(col, row):
        # if (col < 1 || col > 7 || row < 1 || row > 7):
            # return false
        # else:
            # return self.boardArray[col][row]

    # def possibleMoves(col, row):
        # if current_player == 1:
            # if getPieces(col + 1, row + 1) == 0:
                # self.move_list.add(Qpoint(col + 1, row + 1))
            # if getPieces(col - 1, row + 1) == 0:
                # self.move_list.add(Qpoint(col - 1, row + 1))
        # elif current_player == 2:


    def keyPressEvent(self, event):
        # processes key press events if you would like to do any
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
            self.try_move(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.try_move(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.try_move(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.try_move(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)

    def clear_board(self):
        '''clears pieces from the board'''
        # todo write code to reset game

    def try_move(self, new_x, new_y):
        '''tries to move a piece'''

    def draw_grid(self, painter):
        # draw all the squares on the board
        # todo set the default colour of the brush
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                if (row + col) % 2 == 0:
                    colour = Qt.white
                else:
                    colour = Qt.black
                painter.save()
                painter.translate(col * self.square_width(), row * self.square_height())
                painter.setBrush(colour)
                painter.fillRect(0, 0, self.square_width(), self.square_height(), colour)
                painter.restore()

    def draw_pieces(self, painter):
        # draw the prices on the board
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.restore()
                painter.save()
                painter.translate(col * self.square_width(), row * self.square_height())
                if self.boardArray[row][col] == 1:
                    print("BLUE")
                    colour = Qt.blue
                elif self.boardArray[row][col] == 2:
                    print("RED")
                    colour = Qt.red
                else:
                    continue
                painter.setBrush(colour)
                if self.boardArray[row][col] > 0:
                    radius_x = self.square_height() / 2
                    radius_y = self.square_width() / 2
                    center = QPoint(radius_y, radius_x)
                    painter.drawEllipse(center, radius_y, radius_x)
