from PyQt5.QtWidgets import QDockWidget, QLabel, QWidget, QVBoxLayout
from board import Board
import sys


class ScoreBoard(QDockWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        self.show()
        self.label_player1 = QLabel("Player1")
        self.label_player2 = QLabel("Player2")
        self.label_score_player1 = QLabel("Score: ")
        self.label_score_player2 = QLabel("Score: ")
        self.label_currentPlayer = QLabel("CurrentPlayer: ")
        self.widget = QWidget(self)
        self.main_layout = QVBoxLayout()
        self.widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label_player1)
        self.main_layout.addWidget(self.label_player2)
        self.main_layout.addWidget(self.label_score_player1)
        self.main_layout.addWidget(self.label_score_player2)
        self.main_layout.addWidget(self.label_currentPlayer)
        self.setWidget(self.widget)

    def center(self):
        '''centers the window on the screen'''

