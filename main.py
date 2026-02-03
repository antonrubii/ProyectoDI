from events import *
from window import *
import styles
from customers import *
from venAux import *
from reports import Reports
from Products import *
from invoice import *

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
        #Insancia de invoice
        self.invoice = Invoice()

        #cargar estilos
        self.setStyleSheet(styles.load_stylesheet())

        # conexiones
        varcli = True
        varPro = True# cuando arranque el programa solo los clientes True
        Events.resizetableSales(self)
        conexion.Conexion.db_connect("./data/bbdd.sqlite")
        Customers.loadTablecli(varcli)
        Products.loadTablePro(varPro)
        Events.resizeTabCustomer(self)
        Events.resizeTabProducts(self)
        self.invoice.loadTablefac()

        #como cargar un combobox desde un array//con coches seria igual o con otra cosacon mas casos
        iva= ["Foods","Furniture","Clothes","Electronic"]
        globals.ui.cmbFamily.addItems(iva)
        # functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.messageAbout)
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestore_Backup.triggered.connect(Events.restoreBackup)

        # --- SECCIÓN REPORTS EN main.py ---
        # 1. Informe de Clientes
        # Como en tu UI 'menuCustomer_Report' es un QMenu, usamos aboutToShow para detectar el clic
        globals.ui.menuCustomer_Report.aboutToShow.connect(self.report.reportCustomers)

        # 2. Informe de Productos
        # Según tu window.py, la acción se llama actionProducts_Report_2
        globals.ui.actionProducts_Report_2.triggered.connect(self.report.reportProducts)

        globals.ui.txtPrice.editingFinished.connect(Products.checkPrice)
        globals.ui.txtDnifac.editingFinished.connect(self.invoice.buscaCli)
        # functions in lineEdit
        globals.ui.txtDnicli.editingFinished.connect(lambda: Customers.checkDni())
        globals.ui.txtNamecli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtNamecli.text(), globals.ui.txtNamecli))
        globals.ui.txtApelcli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(lambda: Customers.checkMail(globals.ui.txtEmailcli.text(), globals.ui.txtEmailcli))
        globals.ui.txtMobilecli.editingFinished.connect(lambda: Customers.checkMobil(globals.ui.txtMobilecli.text(), globals.ui.txtMobilecli))
        globals.ui.txtDnifac.editingFinished.connect(self.invoice.buscaCli)
        # functions of chkHistoricocli
        globals.ui.chkHistoricocli.stateChanged.connect(lambda: Customers.Historicocli())

        # functions combobox
        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(Events.loadMunicli)
        # functions in buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        globals.ui.btnSavecli.clicked.connect( Customers.saveCli)
        globals.ui.btnCleancli.clicked.connect( Customers.cleanCli)
        globals.ui.btnModifcli.clicked.connect( Customers.modifcli)
        globals.ui.btnDelPro.clicked.connect( Products.delPro)
        globals.ui.btnSavePro.clicked.connect( Products.savePro)
        globals.ui.btnDelPro.clicked.connect( Products.delPro)
        globals.ui.btnModifPro.clicked.connect(Products.modifPro)
        #globals.ui.btnSaveFac.clicked.connect( lambda:Invoice.SaveFac(globals.ui.txtDnifac))

        # functions of tables
        globals.ui.tableCustomerlist.clicked.connect(Customers.selectCustomer)
        globals.ui.tableProducts.clicked.connect(Products.selectProduct)
        globals.ui.tableFac.clicked.connect(self.invoice.selectInvoice)
        globals.ui.tableSales.itemChanged.connect(self.invoice.cellChangedSales)

        # Botón Save de la IZQUIERDA (Crea la factura)
        globals.ui.btnSaveFac.clicked.connect(self.invoice.saveInvoice)

        # Botón del CHECK AZUL (Guarda los productos de la tabla)
        globals.ui.btnOk.clicked.connect(self.invoice.saveSales)

        # Botón para limpiar (el de la flecha circular)
        globals.ui.btnCleancli_4.clicked.connect(self.invoice.cleanFac)

        # Eventos Facturación en main.py
       #globals.ui.btnSaveFac.clicked.connect(Invoice.saveInvoice)  # Conecta el botón de guardar factura
        globals.ui.tableFac.clicked.connect(Invoice.selectInvoice)  # Conecta el click en la tabla

        # Mejoramos el aspecto de la barra de estado
        self.labelstatus = QtWidgets.QLabel("Listo")
        globals.ui.statusbar.addPermanentWidget(self.labelstatus)
        globals.ui.statusbar.setStyleSheet("background-color: white; border-top: 1px solid #D2D2D7;")


        #functions status bar
        Events.loadStatubar(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
