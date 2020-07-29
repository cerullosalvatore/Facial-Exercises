import os

from PyQt5 import QtWidgets, uic

from Controllers.CameraError import Ui_CameraError
from Controllers.VideoTraining import Ui_VideoTraining
from Model.ExerciseManager import ExerciseManager
from Model.MetricLearner import MetricLearner
from Controllers.Decription import Ui_Description
from Controllers.RemovePage import Ui_Remove


class Ui_settingss(QtWidgets.QDialog):
    def __init__(self, category, name):
        super().__init__()
        uic.loadUi('View\Settings.ui', self)
        self._exerciseCategory = category
        self._exerciseName = name
        self.initialize()
        self.setAction()
        self.exec_()
        #self.show()

    def initialize(self):
        if len(os.listdir("Exercises"+'\\'+self._exerciseCategory+'\\'+self._exerciseName+"\\Correct\\Training"))>0  and len(os.listdir("Exercises"+'\\'+self._exerciseCategory+'\\'+self._exerciseName+"\\Bad\\Training"))>0 :
            self.pushButton_3.setEnabled(True)
        else:
            self.pushButton_3.setEnabled(False)

    def setAction(self):
        # Imposto le azioni per gli elementi della GUI che generano eventi
        self.pushButton_2.clicked.connect(lambda: self.createNewVideo("Correct"))
        self.pushButton_6.clicked.connect(lambda: self.createNewVideo("Bad"))
        self.pushButton_4.clicked.connect(self.modDescription)
        self.pushButton_3.clicked.connect(self.trainLearner)
        self.pushButton.clicked.connect(self.removeVideo)
        self.pushButton_5.clicked.connect(self.close)

    def createNewVideo(self, typeVideo):
        exerciseManager = ExerciseManager(self._exerciseCategory,self._exerciseName)
        res = exerciseManager.insert_new_video(typeVideo)
        if res != 0:
            self._windowVideoChoice = Ui_VideoTraining(self._exerciseCategory, self._exerciseName, typeVideo)
        else:
            self.error_message = Ui_CameraError()

        self.initialize()

    def removeVideo(self):
        self.window_remove = Ui_Remove(self._exerciseCategory, self._exerciseName)

    def modDescription(self):
        self.window_modify = Ui_Description(self._exerciseCategory, self._exerciseName)

    def trainLearner(self):
        exerciseManager = ExerciseManager(self._exerciseCategory, self._exerciseName)
        metricLearner = MetricLearner()
        metricLearner.train_metric_learner_supervised(exerciseManager.get_landmarks()[2],exerciseManager.get_landmarks()[3], "Exercises"+'\\'+self._exerciseCategory+'\\'+self._exerciseName+'\\')
