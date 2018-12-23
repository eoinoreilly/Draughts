'''__main__.py'''

from PyQt5.QtWidgets import QApplication
from draughts import Draughts
import sys

app = QApplication([])
draughts = Draughts()
sys.exit(app.exec_())
