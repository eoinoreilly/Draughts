'''board.py'''

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, pyqtSlot
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame, QLabel, QMessageBox
from piece import Piece
from player import Player


class Board(QFrame):
    msg2StatusBar = pyqtSignal(str)
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    updateActivePlayer = pyqtSignal(str)  # signal sent when there is a new active player
    updateScore = pyqtSignal(str)

    boardWidth = 8
    boardHeight = 8
    timerSpeed = 1000  # the timer updates ever 1 second

    def __init__(self, parent):
        super().__init__(parent)
        self.init_board()

    def init_board(self):
        # initiates board
        self.timer1 = QBasicTimer()
        self.timer2 = QBasicTimer()
        self.counter1 = 300  # the number the counter will count down from
        self.counter2 = 300
        self.isWaitingAfterLine = False
        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clicks = 0
        self.selectedPiece, self.fromRow, self.fromCol = 0, 0, 0
        self.currentSquare = ()
        self.selectedSquare = ()
        self.pieceCaptured = False
        self.currentPlayer = Player.Player1 # Defaut Start
        self.turn = 0
        self.pieceSelected = False
        self.updateActivePlayer.emit(self.currentPlayer.name)

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
        self.start()  # start the game which will start the timer

    def paintEvent(self, event):
        # paints the board and the pieces of the game
        painter = QPainter(self)
        # rect = self.contentRect()
        self.draw_grid(painter)
        self.draw_pieces(painter)

    def timerEvent(self, event):
        # this event is automatically called when the timer is updated. based on the timerSpeed variable
        # todo adapt this code to handle your timers
        if event.timerId() == self.timer1.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.counter1 == 0:
                self.msg2StatusBar.emit("Player2, you win!")
                win_msg = QMessageBox()
                win_msg.setIcon(QMessageBox.Information)
                win_msg.setText("Winner")
                win_msg.setInformativeText("Congratulations\nPlayer2 is the Winner")
                win_msg.setWindowTitle("Winner")
                win_msg.addButton(QMessageBox.Reset)
                win_msg.buttonClicked.connect(self.reset)
                win_msg.exec_()
                self.timer1.stop()

            self.counter1 = self.counter1 - 1
            self.updateTimerSignal.emit(self.counter1)
            
        elif event.timerId() == self.timer2.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.counter2 == 0:
                self.msg2StatusBar.emit("Player1, you win!")
                win_msg = QMessageBox()
                win_msg.setIcon(QMessageBox.Information)
                win_msg.setText("Winner")
                win_msg.setInformativeText("Congratulations\nPlayer1 is the Winner")
                win_msg.setWindowTitle("Winner")
                win_msg.addButton(QMessageBox.Reset)
                win_msg.buttonClicked.connect(self.reset)
                win_msg.exec_()
                self.timer2.stop()

            self.counter2 = self.counter2 - 1
            self.updateTimerSignal.emit(self.counter2)

        else:
            super(Board, self).timerEvent(event)  # other wise pass it to the super class for handling

    def mousePressEvent(self, event):
        '''
        Main game play is contained here.  Player turns, game play flags, scores
        and captures are all part of the mousePressEvent.
        '''
        row, col = self.mouse_pos_to_col_row(event)
        self.currentSquare = (row, col)

        # Set expected player and expected player piece
        if self.player_turn() == 0:  # We start with Player 1
            self.currentPlayer = Player.Player1
            player_piece = Piece.Blue

        else:
            self.currentPlayer = Player.Player2
            player_piece = Piece.Red

        # If player begins by selecting an empty square, create error pop up
        if self.clicks == 0 and self.get_pieces(row, col) == 0:
            QMessageBox.about(self, "Error", "You must select a piece first")
            return

        # Ensure Player selects their own piece
        if self.pieceSelected == False and ((self.currentPlayer.name == 'Player1' and self.boardArray[row][col] != 1)
          or (self.currentPlayer.name == 'Player2' and self.boardArray[row][col] != 2)):
            QMessageBox.about(self, "Error", "{} must select a {} piece".format(self.currentPlayer.name, player_piece.name))
            return

        # For the fist click of each player, we store the various parameters
        # for use later in the method.  Here we also highlight the selected
        # piece
        if self.clicks == 0:
            self.clicks += 1
            self.fromRow, self.fromCol = row, col
            self.selectedSquare = (row, col)
            self.selectedPiece = self.boardArray[row][col]
            self.boardArray[row][col] = 3
            self.pieceSelected = True

        # Allow player to deselect a square
        elif self.pieceSelected and (self.selectedSquare == self.currentSquare):
            self.boardArray[row][col] = self.selectedPiece
            self.pieceSelected = False
            self.clicks = 0

        # After Player has selected a piece, we parse the game play logic to
        # dtermine valid moves, captured pieces and scoring
        elif self.clicks >= 1:
            self.clicks += 1

            # We check here if it's a valid move, do not proceed if not.
            #
            if self.is_valid_move(self.selectedSquare, self.currentSquare, self.currentPlayer):
                # We move the selected peice to the target row/col in the array
                # and mark the source square as empty (0)
                self.boardArray[row][col] = self.selectedPiece
                self.boardArray[self.fromRow][self.fromCol] = 0

                # Remove the captured piece, opposite logic for each player
                if self.pieceCaptured:
                    if self.currentPlayer.name == 'Player1':
                        # Update the Player score
                        self.updateScore.emit(self.currentPlayer.name)
                        # We've moved to the right of the board
                        if col > self.fromCol:
                            self.boardArray[row - 1][col - 1] = 0
                        else:
                            self.boardArray[row - 1][col + 1] = 0

                    if self.currentPlayer.name == 'Player2':
                        # Update the Player score
                        self.updateScore.emit(self.currentPlayer.name)
                        # We've moved to the right of the board
                        if col > self.fromCol:
                            self.boardArray[row + 1][col - 1] = 0
                        else:
                            self.boardArray[row + 1][col + 1] = 0
                # Reset flags
                self.pieceCaptured = False
                self.clicks = 0
                self.turn += 1

                if self.currentPlayer.name == 'Player1':
                    self.timer1.stop()
                    self.updateActivePlayer.emit('Player2')
                    self.msg2StatusBar.emit("Player2, it's your turn!")
                    self.timer2.start(Board.timerSpeed, self)

                else:
                    self.timer2.stop()
                    self.updateActivePlayer.emit('Player1')
                    self.msg2StatusBar.emit("Player1, it's your turn!")
                    self.timer1.start(Board.timerSpeed, self)

                # Reset flag for next player
                self.pieceSelected = False
            else:
                QMessageBox.about(self, "Error", "{} invalid move".format(self.currentPlayer.name))
        # Update the board
        self.update()

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
        self.msg2StatusBar.emit("{}, it's your turn!".format(self.currentPlayer.name))
        self.timer1.start(Board.timerSpeed, self)

    def pause(self):
        # pauses game

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer1.stop()
            self.timer2.stop()
            self.msg2StatusBar.emit("Paused on {}'s turn.".format(self.currentPlayer.name))

        else:
            if self.currentPlayer.name == 'Player1':
                self.timer1.start(Board.timerSpeed, self)
                
            elif self.currentPlayer.name == 'Player2':
                self.timer2.start(Board.timerSpeed, self)
            
            self.msg2StatusBar.emit("{}, it's your turn!".format(self.currentPlayer.name))
        self.update()

    def make_connection(self, draughts):
        draughts.resetGame.connect(self.reset)

    @pyqtSlot()
    def reset(self):
        '''
        Reset Game
        '''
        self.init_board()
        self.update()

    def opponent_adjacent(self, player, current_square):
        '''
        Check if there is an opponent diagonally adjacent
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
            if (self.boardArray[current_square[0] + 1][current_square[1] - 1] == 2
                or self.boardArray[current_square[0] + 1][current_square[1] + 1] == 2
                ):
                return True
        if player.name == 'Player2':
            # Only look to the left column if we're on the right edge of the board
            if current_square[1] == 7:
                if self.boardArray[current_square[0] - 1][6] == 1:
                    return True
                return False
            # Only look to the right column if we're on the left edge of the board
            if current_square[1] == 0:
                if self.boardArray[current_square[0] - 1][1] == 1:
                    return True
                return False
            if (self.boardArray[current_square[0] - 1][current_square[1] - 1] == 1
                or self.boardArray[current_square[0] - 1][current_square[1] + 1] == 1
                ):
                return True
        return False

    def is_valid_move(self, from_square, to_square, player):
        '''
        Valid moves will change depending on whether there is an opponent
        adjacent or not, or if the target square is empty or not.
        '''
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
                  and self.get_pieces(to_square[0], to_square[1]) == 0):
                    self.pieceCaptured = True
                    return True

                if ((((from_square[0] + 1, from_square[1] + 1) == to_square)
                  or ((from_square[0] + 1, from_square[1] - 1) == to_square))
                  and self.get_pieces(to_square[0], to_square[1]) == 0):
                    self.pieceCaptured = False
                    return True

            else:
                return False

        if player.name == 'Player2':
            # If there's no adjacent opponent, valid move is 1 diagonal forward
            # as long as destination has no piece
            if not opponent_adj:
                if ((((from_square[0] - 1,from_square[1] + 1) == to_square)
                  or (from_square[0] - 1, from_square[1] - 1) == to_square)
                  and self.get_pieces(to_square[0], to_square[1]) == 0):
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
                return False

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

