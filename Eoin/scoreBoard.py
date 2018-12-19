from PyQt5.QtWidgets import QDockWidget, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt
# from board import Board
import sys


class ScoreBoard(QDockWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # initiates ScoreBoard
        self.p1_score = 0
        self.p2_score = 0
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')
        self.widget = QWidget(self)
        self.widget.setMinimumSize(150,150) # Set minimum width to prevent text overflow
        self.main_layout = QVBoxLayout()

        self.label_player1 = QLabel("Player1\nScore\n\n{}".format(self.p2_score))
        self.label_player1.setStyleSheet('')
        self.label_player1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_player1.setStyleSheet('font-weight: bold; background: yellow')

        self.label_player2 = QLabel("Player2\nScore\n\n{}".format(self.p2_score))
        self.label_player2.setStyleSheet('')
        self.label_player2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.label_currentPlayer = QLabel("CurrentPlayer: ")
        self.label_click_location = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label_player1)
        self.main_layout.addWidget(self.label_player2)
        self.main_layout.addWidget(self.label_currentPlayer)
        self.main_layout.addWidget(self.label_click_location)
        self.main_layout.addWidget(self.label_timeRemaining)
        self.setWidget(self.widget)
        self.show()

    def make_connection(self, board):
        # this handles a signal sent from the board class
        # when the clickLocationSignal is emitted in board the set_click_location slot receives it
        board.clickLocationSignal.connect(self.set_click_location)
        # when the updateTimerSignal is emitted in the board the set_time_remaining slot receives it
        board.updateTimerSignal.connect(self.set_time_remaining)
        board.updateActivePlayer.connect(self.set_player_highlight)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the right type
    def set_click_location(self, click_loc):
        # updates the label to show the click location
        self.label_click_location.setText("Click Location:\n" + click_loc)

    @pyqtSlot(int)
    def set_time_remaining(self, time_remaining):
        # updates the time remaining label to show the time remaining
        # Keep the changing value on a new line so as not to keep altering the width of the QDockWidget
        
        update = "Time Remaining:\n" + str(time_remaining)
        self.label_timeRemaining.setText(update)
        # self.redraw()

    @pyqtSlot(str)
    def set_player_highlight(self, player):
        print("GOT HERE??")
        
        if player == 'Player1':
            self.label_player1.setStyleSheet('font-weight: bold; background: yellow')
            self.label_player2.setStyleSheet('')
            self.update()
            
        elif player == 'Player2':
            self.label_player2.setStyleSheet('font-weight: bold; background: yellow')
            self.label_player1.setStyleSheet('')
            self.update()
