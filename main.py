from events import *
from window import *
import styles
from customers import *
from venAux import *
from reports import Reports

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # instance
        globals.vencal = Calendar()
        globals.about = dlgAbout()
        globals.dlgOpen = FileDialogOpen()
        self.report = Reports()

        #cargar estilos
        self.setStyleSheet(styles.load_stylesheet())

        # conexiones
        varcli = True  # cuando arranque el programa solo los clientes True
        Conexion.db_conexion(self)
        Customers.loadTablecli(varcli)
        Events.resizeTabCustomer(self)


        #como cargar un combobox desde un array//con coches seria igual o con otra cosacon mas casos
        iva= ["4%","12%","21%"]
        globals.ui.cmbIVA.addItems(iva)
        # functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.messageAbout)
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestore_Backup.triggered.connect(Events.restoreBackup)

        globals.ui.actionCustomer_Report.triggered.connect(self.report.reportCustomers)



        # functions in lineEdit
        globals.ui.txtDnicli.editingFinished.connect(lambda: Customers.checkDni())
        globals.ui.txtNamecli.editingFinished.connect(
            lambda: Customers.capitalizar(globals.ui.txtNamecli.text(), globals.ui.txtNamecli)
        )
        globals.ui.txtApelcli.editingFinished.connect(
            lambda: Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli)
        )
        globals.ui.txtEmailcli.editingFinished.connect(
            lambda: Customers.checkMail(globals.ui.txtEmailcli.text())
        )
        globals.ui.txtMobilecli.editingFinished.connect(
            lambda: Customers.checkMobil(globals.ui.txtMobilecli.text())
        )

        # functions of chkHistoricocli
        globals.ui.chkHistoricocli.stateChanged.connect(lambda: Customers.Historicocli())

        # functions combobox
        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(events.Events.loadMunicli)

        # functions in buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        globals.ui.btnSavecli.clicked.connect( Customers.saveCli)
        globals.ui.btnCleancli.clicked.connect( Customers.cleanCli)
        globals.ui.btnModifcli.clicked.connect( Customers.modifcli)

        # functions of tables
        globals.ui.tableCustomerlist.clicked.connect(Customers.selectCustomer)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
