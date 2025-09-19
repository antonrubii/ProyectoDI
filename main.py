import sys
import globals
from events import *
from window import *
from Customers import *

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        #functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)

        #functions in lineEdit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        #otra opción pasar self.ui
        #Customers.conexiones(self.ui)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())



