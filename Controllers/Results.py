import os
from pathlib import Path

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap

from Controllers.VideoTraining import Ui_VideoTraining


class Ui_Results(QtWidgets.QDialog):
    def __init__(self, res, type, name ):
        super().__init__()
        uic.loadUi('View\Results.ui', self)
        self.results = res
        self._type = type
        self._name = name
        self.setAction()
        self.setInitialize()
        self.exec_()

    def setAction(self):
        # Imposto le azioni per gli elementi della GUI che generano eventi
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.changeResult)


    def setInitialize(self):
        if self.results[0] == 0:
            self.label.setText("ESERCIZIO NON ESEGUITO CORRETTAMENTE!")
            pixmap = QPixmap('View\Icons\error.png')
            self.label_2.setPixmap(pixmap)
            self.label_14.setPixmap(pixmap)
        else:
            self.label.setText("COMPLIMENTI! HAI ESEGUITO L'ESERCIZIO CORRETTAMENTE!")
            pixmap = QPixmap('View\Icons\correct.png')
            self.label_2.setPixmap(pixmap)
            self.label_14.setPixmap(pixmap)

        self.label_3.setText(self.results[3])
        self.label_5.setText(self.results[1])
        self.label_7.setText(self.results[4])
        self.label_12.setText(self.results[2])

    def changeResult(self):
        if self.results[0] == 0:
            files = os.listdir("Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Correct")
            os.replace("Exercises/temp.mp4", "Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Correct" + "\\" + str(int(len(files)/2)) + ".mp4")
            os.replace("Exercises/temp.npy", "Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Correct" + "\\" + str(int(len(files)/2)) + ".npy")
            os.replace("Exercises/temp_init.png", "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + "Correct" + "\\Training\\temp_init.png")
            os.replace("Exercises/temp_fin.png", "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + "Correct" + "\\Training\\temp_fin.png")
            os.replace("Exercises/temp_fin.npy", "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + "Correct" + "\\Training\\temp_fin.npy")
            self._windowVideoChoice = Ui_VideoTraining(self._type, self._name, "Correct")

        else:
            files =  os.listdir("Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Bad")
            os.replace("Exercises/temp.mp4", "Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Bad" + "\\" + str(int(len(files)/2)) + ".mp4")
            os.replace("Exercises/temp.npy", "Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Bad" + "\\" + str(int(len(files)/2)) + ".npy")
            os.replace("Exercises/temp_init.png", "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + "Bad" + "\\Training\\temp_init.png")
            os.replace("Exercises/temp_fin.png", "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + "Bad" + "\\Training\\temp_fin.png")
            os.replace("Exercises/temp_fin.npy", "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + "Bad" + "\\Training\\temp_fin.npy")
            self._windowVideoChoice = Ui_VideoTraining(self._type, self._name, "Bad")
        self.pushButton_2.setEnabled(False)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        my_file = Path("Exercises/temp.mp4")
        if my_file.exists():
            os.remove("Exercises/temp.mp4")
        my_file = Path("Exercises/temp.npy")
        if my_file.exists():
            os.remove("Exercises/temp.npy")
