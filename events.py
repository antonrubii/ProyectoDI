import sys
import globals
from venAux import *

class Events:
    @staticmethod
    def messageExit(self=None):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
            mbox.setWindowTitle('Exit')
            mbox.setText('Are you sure you want to exit?')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            #si quisiese en español pondría las dos líneas siguientes
            #mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            #mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
            mbox.resize(600, 800)  # no funciona si no usa QDialog porque QMessageBox lo tienen bloqueado
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
            else:
                mbox.hide()
        except Exception as e:
            print("error en salida", e)

    def openCalendar(self):
        try:
            globals.vencal.show()

        except Exception as e:
            print("error en calendario", e)
