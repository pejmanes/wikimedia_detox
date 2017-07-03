# coding: utf-8

import sys, os
from PyQt5.QtWidgets import QApplication
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from GUI import gui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = gui.MainWindow()
    sys.exit(app.exec_())
