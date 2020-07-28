import sys
from PyQt5 import QtWidgets

from Controllers.MainPage import Ui


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

if __name__ == "__main__":
    main()