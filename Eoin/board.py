from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame, QLabel, QMessageBox
from piece import Piece
from player import Player
from scoreBoard import ScoreBoard
import logging


class Board(QFrame):
    msg2StatusBar = pyqtSignal(str)
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location
    updateActivePlayer = pyqtSignal(str) # signal sent when there is a new active player

    boardWidth = 8
    boardHeight = 8
    timerSpeed = 1000  # the timer updates ever 1 second
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
        self.reset()
        self.start()  # start the game which will start the timer
        self.clicks = 0
        self.selectedPiece, self.fromRow, self.fromCol = 0, 0, 0
        self.selectedSquare = ()
        self.pieceCaptured = False
        self.currentPlayer = Player.Player1 # Defaut Start
        self.turn = 0
        self.pieceSelected = False
        self.updateActivePlayer.emit(self.currentPlayer.name)
        print("CURRENT PLAYER:  {}".format(self.currentPlayer.name))

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

    def paintEvent(self, event):
        # paints the board and the pieces of the game
        painter = QPainter(self)
        # rect = self.contentRect()
        self.draw_grid(painter)
        self.draw_pieces(painter)

    def timerEvent(self, event):
        # this event is automatically called when the timer is updated. based on the timerSpeed variable
        # todo adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")

            Board.counter = Board.counter - 1
            self.updateTimerSignal.emit(Board.counter)

        else:
            super(Board, self).timerEvent(event)  # other wise pass it to the super class for handling

    def mousePressEvent(self, event):
        row, col = self.mouse_pos_to_col_row(event)
        square = (row, col)

        # Set expected player and expected player piece
        if self.player_turn() == 0:  # We start with Player 1
            self.currentPlayer = Player.Player1
            player_piece = Piece.Blue

        else:
            self.currentPlayer = Player.Player2
            player_piece = Piece.Red

        # If player begins by selecting an empty square, create pop up
        if self.clicks == 0 and self.get_pieces(row, col) == 0:
            print(self.clicks)
            QMessageBox.about(self, "Error", "You must select a piece first")
            return

        # Ensure Player selects their own piece
        if self.pieceSelected == False and ((self.currentPlayer.name == 'Player1' and self.boardArray[row][col] != 1)
          or (self.currentPlayer.name == 'Player2' and self.boardArray[row][col] != 2)):
            QMessageBox.about(self, "Error", "{} must select a {} piece".format(self.currentPlayer.name, player_piece.name))
            return

        if self.clicks == 0:
            QMessageBox.about(self, "Player Timer", "{} Timer begins".format(self.currentPlayer.name))
            self.clicks += 1
            # Store current location value before changing the colour to highlight
            self.fromRow, self.fromCol = row, col
            self.selectedSquare = (row, col)
            self.selectedPiece = self.boardArray[row][col]
            self.boardArray[row][col] = 3
            self.pieceSelected = True

        elif self.clicks >= 1:
            self.clicks += 1
            if self.is_valid_move(self.selectedSquare, square, self.currentPlayer):
                self.boardArray[row][col] = self.selectedPiece
                self.boardArray[self.fromRow][self.fromCol] = 0
                # Remove the captured piece, opposite logic for each player
                if self.pieceCaptured:
                    if self.currentPlayer.name == 'Player1':
                        # TODO:  Update Score for player
                        if col > self.fromCol: # We've moved to the right of the board
                            self.boardArray[row - 1][col - 1] = 0

                        else:
                            self.boardArray[row - 1][col + 1] = 0

                    if self.currentPlayer.name == 'Player2':
                        # TODO:  Update Score for player
                        if col > self.fromCol: # We've moved to the right of the board
                            self.boardArray[row + 1][col - 1] = 0

                        else:
                            self.boardArray[row + 1][col + 1] = 0

                self.clicks = 0
                self.turn += 1

                if self.currentPlayer.name == 'Player1':
                    self.updateActivePlayer.emit('Player2')

                else:
                    self.updateActivePlayer.emit('Player1')

                self.pieceSelected = False  # Reset flag for next player
        # ScoreBoard.make_connection
        self.update()

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

    def draw_grid(self, painter):
        # draw all the squares on the board
        # todo set the default colour of the brush
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                if (row + col) % 2 == 0:
                    colour = QColor(255, 255, 204)

                else:
                    colour = QColor(204, 255, 204)

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
                    colour = QColor(128, 179, 255)

                elif self.boardArray[row][col] == 2:
                    colour = QColor(255, 128, 128)

                elif self.boardArray[row][col] == 3:
                    colour = QColor(244, 170, 66)

                else:
                    continue

                painter.setBrush(colour)

                if self.boardArray[row][col] > 0:
                    radius_x = int(self.square_height() / 2)
                    radius_y = int(self.square_width() / 2)
                    center = QPoint(radius_y, radius_x)
                    painter.drawEllipse(center, 9 * radius_y / 10, 9 * radius_x / 10)

    def square_width(self):
        # returns the width of one square in the board
        return self.contentsRect().width() / Board.boardWidth

    def square_height(self):
        # returns the height of one square in the board
        return self.contentsRect().height() / Board.boardHeight

    def print_board_array(self):
        # prints the boardArray in an attractive way
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def player_turn(self):
        return self.turn % 2

    def mouse_pos_to_col_row(self, event):
        # convert the mouse click event to a row and column
        self.click_row = int(event.y() / self.square_height())
        self.click_col = int(event.x() / self.square_width())
        return self.click_row, self.click_col

    def start(self):
        # starts game
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.reset()
        self.msg2StatusBar.emit(str("status message"))
        self.timer.start(Board.timerSpeed, self)
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
            self.timer.start(Board.timerSpeed, self)
            self.msg2StatusBar.emit(str("status message"))
        self.update()

    def reset(self):
        '''clears pieces from the board'''
        # todo write code to reset game

    def opponent_adjacent(self, player, current_square):
        ''' Check if there is an opponent diagonally adjacent
        '''
        if player.name == 'Player1':
            # Only look to the left column if we're on the right edge of the board
            if current_square[1] == 7:
                if self.boardArray[current_square[0] + 1][6] == 2:
                    return True
                return False
            # Only look to the right column if we're on the left edge of the board
            if current_square[1] == 0:
                if self.boardArray[current_square[0] + 1][1] == 2:
                    return True
                return False
            if (self.boardArray[current_square[0] + 1][current_square[1] - 1]
                or self.boardArray[current_square[0] + 1][current_square[1] + 1]
                ) == 2:
                return True
        if player.name == 'Player2':
            # Only look to the left column if we're on the right edge of the board
            if current_square[1] == 7:
                if self.boardArray[current_square[0] - 1][6] == 2:
                    return True
                return False
            # Only look to the right column if we're on the left edge of the board
            if current_square[1] == 0:
                if self.boardArray[current_square[0] - 1][1] == 2:
                    return True
                return False
            if (self.boardArray[current_square[0] - 1][current_square[1] - 1]
                or self.boardArray[current_square[0] - 1][current_square[1] + 1]
                ) == 1:
                return True
        return False

    def is_valid_move(self, from_square, to_square, player):
        opponent_adj = self.opponent_adjacent(player, from_square)

        if player.name == 'Player1':
            # If there's no adjacent opponent, valid move is 1 diagonal forward
            # as long as destination has no piece
            if not opponent_adj:
                if ((((from_square[0] + 1, from_square[1] + 1) == to_square)
                  or (from_square[0] + 1, from_square[1] - 1) == to_square)
                  and self.get_pieces(to_square[0], to_square[1]) == 0):
                    return True
            # If we have an adjacent opponent, we can move 1 diagonal forward
            # or 2 diagonal forward as long as destination has no piece
            if opponent_adj:
                if ((((from_square[0] + 2, from_square[1] + 2)  == to_square)
                  or ((from_square[0] + 2, from_square[1] - 2) == to_square))
                  and self.get_pieces(to_square[0], to_square[1] == 0)):
                    self.pieceCaptured = True
                    return True

                if ((((from_square[0] + 1, from_square[1] + 1) == to_square)
                  or ((from_square[0] + 1, from_square[1] - 1) == to_square))
                  and self.get_pieces(to_square[0], to_square[1] == 0)):
                    self.pieceCaptured = False
                    return True

            else:
                return QMessageBox.about(self, "Error", "{} invalid move".format(player.name))

        if player.name == 'Player2':
            # If there's no adjacent opponent, valid move is 1 diagonal forward
            # as long as destination has no piece
            if not opponent_adj:
                if ((((from_square[0] - 1,from_square[1] + 1) == to_square)
                  or (from_square[0] - 1, from_square[1] - 1) == to_square)
                  and self.get_pieces(to_square[0], to_square[1])) == 0:
                    return True

            # If we have an adjacent opponent, we can move 1 diagonal forward
            # or 2 diagonal forward as long as destination has no piece
            if opponent_adj:
                if ((((from_square[0] - 2,from_square[1] + 2)  == to_square)
                  or ((from_square[0] - 2, from_square[1] - 2) == to_square))
                  and self.get_pieces(to_square[0], to_square[1]) == 0):
                    self.pieceCaptured = True
                    return True

                if ((((from_square[0] - 1,from_square[1] + 1) == to_square)
                  or ((from_square[0] - 1, from_square[1] - 1) == to_square))
                  and self.get_pieces(to_square[0], to_square[1]) == 0):
                    self.pieceCaptured = False
                    return True

            else:
                return QMessageBox.about(self, "Error", "{} invalid move".format(player.name))

        return False

    def get_pieces(self, row, col):
        if col < 0 or col > 7 or row < 0 or row > 7:
            return False

        else:
            return self.boardArray[row][col]

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

    # def possible_moves(col, row):
        # if current_player == 1:
            # if get_pieces(col + 1, row + 1) == 0:
                # self.move_list.add(Qpoint(col + 1, row + 1))

            # if get_pieces(col - 1, row + 1) == 0:
                # self.move_list.add(Qpoint(col - 1, row + 1))

        # elif current_player == 2:
