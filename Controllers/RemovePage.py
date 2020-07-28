import os

from PyQt5 import QtWidgets, uic

from Model.ExerciseManager import ExerciseManager


class Ui_Remove(QtWidgets.QDialog):
    def __init__(self, category, name):
        super().__init__()
        uic.loadUi('View\RemoveVideo.ui', self)
        self._exerciseCategory = category
        self._exerciseName = name
        self._currentExercise = None
        self.setAction()
        self.initialize_gui()
        self.exec_()


    def initialize_gui(self):
        self.comboBox.addItems(next(os.walk("./Exercises/"+self._exerciseCategory+"/"+self._exerciseName))[1])
        self.changeCategory()

    def setAction(self):
        # Imposto le azioni per gli elementi della GUI che generano eventi
        self.pushButton.clicked.connect(self.removeVideo)
        self.pushButton_2.clicked.connect(self.close)
        self.comboBox.currentIndexChanged.connect(self.changeCategory)

    def removeVideo(self):
        if self.comboBox_2.currentText():
            self._currentExercise = ExerciseManager(self._exerciseCategory, self._exerciseName)
            self._currentExercise.remove_video(self.comboBox.currentText(), self.comboBox_2.currentText()[:-4])
            self.close()

    def changeCategory(self):
        self.comboBox_2.clear()
        files = [fname for fname in sorted(os.listdir("./Exercises/"+self._exerciseCategory+"/"+self._exerciseName+"/"+self.comboBox.currentText()),  key = len) if fname.endswith('.mp4')]
        x = len(files)
        self.comboBox_2.addItems(files)
        self.comboBox_2.setCurrentIndex(0)