import os
from os import path

from PyQt5 import QtWidgets, uic, QtMultimedia, QtCore

from Model.ExerciseManager import ExerciseManager
from Controllers.Results import Ui_Results
from Controllers.Settings import Ui_settingss


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi('View\MainPage.ui', self)
        self._currentExercise = None
        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.ui.widget_8)
        self.initialize_gui()
        self.setAction()
        self.show()

    def initialize_gui(self):
        diect = []
        for file in os.listdir("Exercises"):
            if not(file.endswith(".npy")) and not(file.endswith(".png")) and not(file.endswith(".mp4")):
                diect.append(file)
        self.comboBox.addItems(diect)
        self.changeCategory()
        self._currentExercise = ExerciseManager(self.comboBox.currentText(), self.comboBox_2.currentText())
        self.play_video(self.comboBox.currentText(), self.comboBox_2.currentText())
        self.label_5.setText(self._currentExercise.get_description())
        if path.exists("Exercises"+'\\'+self.comboBox.currentText()+'\\'+self.comboBox_2.currentText()+"\\TreanedModel.sav"):
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

    def setAction(self):
        # Imposto le azioni per gli elementi della GUI che generano eventi
        self.comboBox.currentIndexChanged.connect(self.changeCategory)
        self.comboBox_2.currentIndexChanged.connect(self.changeExercise)
        self.pushButton_3.clicked.connect(self.show_settings)
        self.pushButton.clicked.connect(self.execute_exercise)
        self.player.stateChanged.connect(self.player.play)

    def changeCategory(self):
        self.comboBox_2.clear()
        self.comboBox_2.addItems(sorted(os.listdir("Exercises"+'\\'+self.comboBox.currentText()+'\\'+self.comboBox_2.currentText()),  key = len))
        self.comboBox_2.setCurrentIndex(0)
        self._currentExercise = ExerciseManager(self.comboBox.currentText(), self.comboBox_2.currentText())

    def changeExercise(self):
        if(self.comboBox_2.currentText()):
            self._currentExercise = ExerciseManager(self.comboBox.currentText(), self.comboBox_2.currentText())
            self.label_5.setText(self._currentExercise.get_description())
            self.play_video(self.comboBox.currentText(), self.comboBox_2.currentText())
        if path.exists("Exercises"+'\\'+self.comboBox.currentText()+'\\'+self.comboBox_2.currentText()+"\\TreanedModel.sav"):
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

    def show_settings(self):
        self.window_setting = Ui_settingss(self.comboBox.currentText(), self.comboBox_2.currentText())

    def play_video(self, category, name):
        file = "Exercises/" + category + "/" + name + "/demo.wmv"
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
        self.player.play()

    def execute_exercise(self):
        self._currentExercise = ExerciseManager(self.comboBox.currentText(), self.comboBox_2.currentText())
        self.result = Ui_Results(self._currentExercise.execute_exercise(), self.comboBox.currentText(), self.comboBox_2.currentText())



