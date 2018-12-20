import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QLabel, QAction, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from board import Board
from scoreBoard import ScoreBoard


class Draughts(QMainWindow):
    resetGame = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # stylesheet = \
        #     ".QWidget {\n" \
        #     + "border: 20px solid black;\n" \
        #     + "border-radius: 4px;\n" \
        #     + "background-color: rgb(255, 255, 255);\n" \
        #     + "}"

        self.init_ui()

    def init_ui(self):
        # initiates application UI
        self.tboard = Board(self)
        # self.tboard.setStyleSheet(stylesheet)
        self.setCentralWidget(self.tboard)

        self.scoreBoard = ScoreBoard()
        self.scoreBoard.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        
        self.reset_button = QPushButton(QIcon("../img/reset.png"), "", self)
        self.reset_button.setToolTip("Reset the game.")
        self.reset_button.clicked.connect(self.reset)
        
        self.pause_button = QPushButton(QIcon("../img/pause_play.png"), "", self)
        self.pause_button.setToolTip("Pause or continue the game.")
        self.pause_button.clicked.connect(self.tboard.pause)

        self.toolbar = self.addToolBar("MainToolBar")
        self.toolbar.setOrientation(Qt.Horizontal)
        self.toolbar.addWidget(self.reset_button)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.pause_button)

        self.statusbar = self.statusBar()
        self.tboard.msg2StatusBar[str].connect(self.statusbar.showMessage)
        self.scoreBoard.make_connection(self.tboard)
        self.tboard.make_connection(self)

        self.tboard.start()

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('DraughtsV3')
        self.show()

    def reset(self):
        '''
        Allow user to reset the game
        '''
        self.scoreBoard.p1_score = 0
        self.scoreBoard.p2_score = 0
        self.scoreBoard.p1_pieces_remaining = 12
        self.scoreBoard.p2_pieces_remaining = 12
        self.scoreBoard.label_player1.setText("Player1\n\nScore {}\n Remaining {}".format(self.scoreBoard.p1_score, self.scoreBoard.p1_pieces_remaining))
        self.scoreBoard.label_player2.setText("Player2\n\nScore {}\n Remaining {}".format(self.scoreBoard.p2_score, self.scoreBoard.p2_pieces_remaining))
        self.resetGame.emit()

    def get_board(self):
        return self.board

    def get_score_board(self):
        return self.scoreBoard

    def center(self):
        # centers the window on the screen
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        center_x = int((screen.width() - size.width()) / 2)
        center_y = int((screen.height() - size.height()) / 2)
        self.move(center_x, center_y)


if __name__ == "__main__":
    app = QApplication([])
    draughts = Draughts()
    sys.exit(app.exec_())
