from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt
from board import Board
from scoreBoard import ScoreBoard
import sys



class Draughts(QMainWindow):

    def __init__(self):
        super().__init__()
        # stylesheet = \
        #     ".QWidget {\n" \
        #     + "border: 20px solid black;\n" \
        #     + "border-radius: 4px;\n" \
        #     + "background-color: rgb(255, 255, 255);\n" \
        #     + "}"

        self.initUI()

    def initUI(self):
        '''initiates application UI'''
        self.tboard = Board(self)
        # self.tboard.setStyleSheet(stylesheet)
        self.setCentralWidget(self.tboard)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        self.resize(800, 800)
        self.setFixedSize(self.size())
        self.center()
        self.setWindowTitle('DraughtsV3')
        self.show()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
