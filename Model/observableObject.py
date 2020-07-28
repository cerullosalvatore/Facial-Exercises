from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty
"""
La classe ObservableObject rappresenta un oggetto osservabile di base.

Questo oggetto avrà un solo valore al quale sarà possibile iscriversi per osservarne i cambiamenti.
Ad ogni cambiamento di _value verrà emesso un segnale in modo tale che gli iscritti ad esso possano ascoltare ed agire 
di conseguenza.
"""
class ObservableObject(QObject):
    valueChanged = pyqtSignal(object)
    def __init__(self, val):
        super().__init__()
        self._value = val

    def register(self, slot):
        """
        Permette di registrarsi al segnale valueChanged
        :param slot:
        """
        self.valueChanged.connect(slot)

    @pyqtProperty(object, notify=valueChanged)
    def value(self):
        """
        Possiamo accedere al valore contenuto in _value solo attraverso questa funzione
        :return:
        """
        return self._value

    @value.setter
    def value(self, newval):
        """
        Possiamo cambiare il valore di _value solo attraverso questa funzione. Ad ogni cambiamento di _value verrà emesso
        un segnale da valueChanger
        :param newval: nuovo valore dell'oggetto osservato.
        """
        self._value = newval
        self.valueChanged.emit(self.value)