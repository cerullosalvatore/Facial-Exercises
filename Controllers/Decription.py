from PyQt5 import QtWidgets, uic

from Model.ExerciseManager import ExerciseManager
from Controllers.RemovePage import Ui_Remove


class Ui_Description(QtWidgets.QDialog):
    def __init__(self, category, name):
        super().__init__()
        uic.loadUi('View\Description.ui', self)
        self._exerciseManager = ExerciseManager(category, name)
        self.textEdit.insertPlainText(self._exerciseManager.get_description())
        self.setAction()
        self.exec_()

    def setAction(self):
        # Imposto le azioni per gli elementi della GUI che generano eventi
        self.pushButton.clicked.connect(self.saveDescription)
        self.pushButton_2.clicked.connect(self.close)

    def saveDescription(self):
        self._exerciseManager.replace_description(self.textEdit.toPlainText())
        self.close()

    def removeVideo(self):
        self.window_remove = Ui_Remove(self._exerciseCategory, self._exerciseName)