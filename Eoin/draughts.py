import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QLabel
from board import Board
from scoreBoard import ScoreBoard


class Draughts(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # initiates application UI
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)
        # dock
        self.scoreBoard = ScoreBoard()
        self.scoreBoard.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        
        self.toolbar = self.addToolBar("MainToolBar")
        self.toolbar.addWidget(QLabel("Some widget"))
        
        self.statusbar = self.statusBar()
        self.tboard.msg2StatusBar[str].connect(self.statusbar.showMessage)
        
        self.tboard.start()
        
        self.resize(800, 800)
        self.center()
        self.setWindowTitle('DraughtsV3')
        self.show()


    def center(self):
        # centers the window on the screen
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


    def get_score_board(self):
        return self.scoreboard


if __name__ == "__main__":
    app = QApplication([])
    draughts = Draughts()
    sys.exit(app.exec_())
