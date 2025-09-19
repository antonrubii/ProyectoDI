import globals
from PyQt6 import QtCore, QtGui, QtWidgets


class Customers:
    @staticmethod
    def checkDni(self=None):
        dni = globals.ui.txtDnicli.text()
        print(dni)
