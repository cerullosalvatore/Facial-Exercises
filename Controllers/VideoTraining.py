import os
from pathlib import Path

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap


class Ui_VideoTraining(QtWidgets.QDialog):
    def __init__(self, type, name, type_video ):
        super().__init__()
        uic.loadUi('View\ConfirmVideo.ui', self)
        self._type = type
        self._type_video = type_video
        self._name = name
        self.setAction()
        self.setInitialize()
        self.exec_()

    def setAction(self):
        # Imposto le azioni per gli elementi della GUI che generano eventi
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.saveVideoTraining)


    def setInitialize(self):
        pixmap = QPixmap("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_init.png")
        self.label.setPixmap(pixmap)
        pixmap = QPixmap("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_fin.png")
        self.label_2.setPixmap(pixmap)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        my_file = Path("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_init.png")
        if my_file.exists():
            os.remove(my_file)
        my_file = Path("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_fin.png")
        if my_file.exists():
            os.remove(my_file)
        my_file = Path("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_fin.npy")
        if my_file.exists():
            os.remove(my_file)
        my_file = Path("Exercises\\temp_init.png")
        if my_file.exists():
            os.remove(my_file)
        my_file = Path("Exercises\\temp_fin.png")
        if my_file.exists():
            os.remove(my_file)
        my_file = Path("Exercises\\temp_fin.npy")
        if my_file.exists():
            os.remove(my_file)

    def saveVideoTraining(self):
        count = 0
        for file in os.listdir("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training"):
            if file.endswith(".npy"):
                count += 1

        os.rename("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_init.png",
                  "Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\" + str(count-1) + "_init.png")
        os.rename("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_fin.png",
                  "Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\" + str(count-1) + "_fin.png")
        os.rename("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\temp_fin.npy",
                  "Exercises" + "\\" + self._type + "\\" + self._name + "\\" + str(self._type_video) + "\\Training\\" + str(count-1) + ".npy")
        self.close()
