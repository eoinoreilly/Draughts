from PyQt5.QtWidgets import QDockWidget, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt
# from board import Board
import sys


class ScoreBoard(QDockWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        '''initiates ScoreBoard UI'''
        self.p1_score = 0
        self.p2_score = 0
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        self.widget = QWidget(self)
        self.widget.setMinimumSize(150,150) # Set minimum width to prevent text overflow
        self.main_layout = QVBoxLayout()

        self.label_player1 = QLabel("Player1\nScore\n\n{}".format(self.p2_score))
        self.label_player1.setStyleSheet('')
        self.label_player1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_player1.setStyleSheet('font-weight: bold; background: yellow')
        # self.label_score_player1 = QLabel(str(0))
        # self.label_score_player1.setStyleSheet('')
        # self.label_score_player1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.label_player2 = QLabel("Player2\nScore\n\n{}".format(self.p2_score))
        self.label_player2.setStyleSheet('')
        self.label_player2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        # self.label_score_player2 = QLabel(str(0))
        # self.label_score_player2.setStyleSheet('')
        # self.label_score_player2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.label_currentPlayer = QLabel("CurrentPlayer: ")
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label_player1)
        # self.main_layout.addWidget(self.label_score_player1)
        self.main_layout.addWidget(self.label_player2)
        # self.main_layout.addWidget(self.label_score_player2)
        self.main_layout.addWidget(self.label_currentPlayer)
        self.main_layout.addWidget(self.label_clickLocation)
        self.main_layout.addWidget(self.label_timeRemaining)
        self.setWidget(self.widget)
        self.show()

    def center(self):
        '''centers the window on the screen'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.updateActivePlayer.connect(self.setPlayerHighlight)

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an arguement of the right type
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:\n" + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining

        Keep the changing value on a new line so as not to keep altering the
        width of the QDockWidget
        '''
        update = "Time Remaining:\n" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        # self.redraw()

    @pyqtSlot(str)
    def setPlayerHighlight(self, player):
        print("GOT HERE??")
        if player == 'Player1':
            self.label_player1.setStyleSheet('font-weight: bold; background: yellow')
            # self.label_score_player1.setStyleSheet('font-weight: bold; background: yellow')
            self.label_player2.setStyleSheet('')
            # self.label_score_player2.setStyleSheet('')
            self.update()
        elif player == 'Player2':
            self.label_player2.setStyleSheet('font-weight: bold; background: yellow')
            # self.label_score_player2.setStyleSheet('font-weight: bold; background: yellow')
            self.label_player1.setStyleSheet('')
            # self.label_score_player1.setStyleSheet('')
            self.update()




