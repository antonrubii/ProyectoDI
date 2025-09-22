from events import *
from window import *
from customers import *
from venAux import *




class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)
        #instance
        globals.vencal = Calendar()

        #functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)

        #functions in lineEdit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        #other opction opción pass, Ex. "self.ui"  ==> customers.conexiones(self.ui)

        #functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())



