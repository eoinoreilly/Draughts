'''scoreBoard.py'''

from PyQt5.QtWidgets import QDockWidget, QLabel, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
import sys


class ScoreBoard(QDockWidget):
    winnerSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # initiates ScoreBoard
        self.player = 'Player1'
        self.p1_score = 0
        self.p2_score = 0
        self.p1_pieces_remaining = 12
        self.p2_pieces_remaining = 12
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')
        self.widget = QWidget(self)
        self.widget.setMinimumSize(150,150) # Set minimum width to prevent text overflow
        self.main_layout = QVBoxLayout()

        # Update score widget with Player Specific scoreing details
        self.label_player1 = QLabel("Player1\n\nScore {}\n Remaining {}".format(self.p1_score, self.p1_pieces_remaining))
        self.label_player1.setStyleSheet('')
        self.label_player1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_player1.setStyleSheet('font-weight: bold; background: rgb(128, 179, 255)')

        self.label_player2 = QLabel("Player2\n\nScore {}\n Remaining {}".format(self.p2_score, self.p2_pieces_remaining))
        self.label_player2.setStyleSheet('')
        self.label_player2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.p1_time_remaining = QLabel("Time\nRemaining:\n300")
        self.p1_time_remaining.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.p1_time_remaining.setStyleSheet('font-weight: bold; background: rgb(128, 179, 255)')

        self.p2_time_remaining = QLabel("Time\nRemaining:\n300")
        self.p2_time_remaining.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label_player1)
        self.main_layout.addWidget(self.p1_time_remaining)
        self.main_layout.addWidget(self.label_player2)
        self.main_layout.addWidget(self.p2_time_remaining)
        self.setWidget(self.widget)
        self.show()

    def make_connection(self, board):
        # this handles a signal sent from the board class
        # when the clickLocationSignal is emitted in board the set_click_location slot receives it
        # when the updateTimerSignal is emitted in the board the set_time_remaining slot receives it
        board.updateTimerSignal.connect(self.set_time_remaining)
        board.updateActivePlayer.connect(self.set_player_highlight)
        board.updateScore.connect(self.updateScore)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the right type
    def updateScore(self, player):
        '''
        pyqtSlot from player class to update the score of the passed player
        '''
        if player == 'Player1':
            self.p1_score += 1
            self.p2_pieces_remaining -= 1
            # We need to update both players, 1 for score and the other for remaining pieces
            self.label_player1.setText("Player1\n\nScore {}\n Remaining {}".format(self.p1_score, self.p1_pieces_remaining))
            self.label_player2.setText("Player2\n\nScore {}\n Remaining {}".format(self.p2_score, self.p2_pieces_remaining))
            if self.p2_pieces_remaining == 0:
                self.winnerSignal.emit("Player1")

        elif player == 'Player2':
            self.p2_score += 1
            self.p1_pieces_remaining -= 1
            # We need to update both players, 1 for score and the other for remaining pieces
            self.label_player1.setText("Player1\n\nScore {}\n Remaining {}".format(self.p1_score, self.p1_pieces_remaining))
            self.label_player2.setText("Player2\n\nScore {}\n Remaining {}".format(self.p2_score, self.p2_pieces_remaining))
            if self.p1_pieces_remaining == 0:
                self.winnerSignal.emit("Player2")


    @pyqtSlot(int)
    def set_time_remaining(self, time_remaining):
        # updates the time remaining label to show the time remaining
        # Keep the changing value on a new line so as not to keep altering the width of the QDockWidget
        if self.player == 'Player1':
            update = "Time\nRemaining:\n" + str(time_remaining)
            self.p1_time_remaining.setText(update)

        elif self.player == 'Player2':
            update = "Time\nRemaining:\n" + str(time_remaining)
            self.p2_time_remaining.setText(update)

    @pyqtSlot(str)
    def set_player_highlight(self, player):
        '''
        pyqtSlot from player class to highlight the active player in the
        scoreBoard widget
        '''
        self.player = player

        if self.player == 'Player1':
            self.label_player1.setStyleSheet('font-weight: bold; background: rgb(128, 179, 255)')
            self.p1_time_remaining.setStyleSheet('font-weight: bold; background: rgb(128, 179, 255)')
            self.label_player2.setStyleSheet('')
            self.p2_time_remaining.setStyleSheet('')

        elif self.player == 'Player2':
            self.label_player2.setStyleSheet('font-weight: bold; background: rgb(255, 128, 128)')
            self.p2_time_remaining.setStyleSheet('font-weight: bold; background: rgb(255, 128, 128)')
            self.label_player1.setStyleSheet('')
            self.p1_time_remaining.setStyleSheet('')
        self.update()
