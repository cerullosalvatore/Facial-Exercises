import os
from pathlib import Path

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap

from Controllers.VideoTraining import Ui_VideoTraining


class Ui_CameraError(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('View\CameraError.ui', self)
        self.pushButton.clicked.connect(self.close)
        self.exec_()
