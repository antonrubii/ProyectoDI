import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import globals
import conexion
import styles
from window import Ui_MainWindow
from events import Events
from customers import Customers
from Products import Products
from invoice import Invoice
from reports import Reports
from venAux import Calendar, dlgAbout, FileDialogOpen


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # --- 1. INSTANCIAS DE COMPONENTES ---
        globals.vencal = Calendar()
        globals.about = dlgAbout()
        globals.dlgOpen = FileDialogOpen()
        self.report = Reports()
        self.invoice = Invoice()

        # --- 2. CONFIGURACIÓN INICIAL Y ESTILOS ---
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_connect("./data/bbdd.sqlite")

        # Ajustar anchos y diseño de tablas
        Events.resizeTabCustomer(self)
        Events.resizeTabProducts(self)
        Events.resizetableSales(self)
        Events.loadStatubar(self)

        # CORRECCIÓN DE CABECERAS (Para que coincidan con los datos de tu imagen)
        headers = ["Surname", "Name", "DNI/NIE", "Mobile", "Province", "City", "Status"]
        globals.ui.tableCustomerlist.setHorizontalHeaderLabels(headers)

        # Cargar datos iniciales en las tablas
        Customers.loadTablecli(True)
        Products.loadTablePro()
        self.invoice.loadTablefac()

        # Cargar combos
        Events.loadProv(self)
        familias = ["", "Foods", "Furniture", "Clothes", "Electronic"]
        globals.ui.cmbFamily.addItems(familias)

        # --- 3. CONEXIÓN DE MENÚS Y TOOLBAR ---
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.messageAbout)
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestore_Backup.triggered.connect(Events.restoreBackup)

        # Menú Reports
        globals.ui.menuCustomer_Report.aboutToShow.connect(self.report.reportCustomers)
        globals.ui.actionProducts_Report_2.triggered.connect(self.report.reportProducts)

        # NUEVO: Report por Provincia (Selector dinámico)
        self.reportProv = QtGui.QAction("Report por Provincia", self)
        globals.ui.menuReports.addAction(self.reportProv)
        self.reportProv.triggered.connect(self.elegirProvincia)

        # --- 4. VALIDACIONES Y BÚSQUEDA DINÁMICA ---
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNamecli.editingFinished.connect(
            lambda: Customers.capitalizar(globals.ui.txtNamecli.text(), globals.ui.txtNamecli))
        globals.ui.txtApelcli.editingFinished.connect(
            lambda: Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(
            lambda: Customers.checkMail(globals.ui.txtEmailcli.text(), globals.ui.txtEmailcli))
        globals.ui.txtMobilecli.editingFinished.connect(
            lambda: Customers.checkMobil(globals.ui.txtMobilecli.text(), globals.ui.txtMobilecli))

        # BUSCADOR DINÁMICO: Filtra clientes mientras escribes el apellido
        globals.ui.txtApelcli.textChanged.connect(Customers.searchDynamic)

        # Facturación y Productos
        globals.ui.txtDnifac.editingFinished.connect(Invoice.buscaCli)
        globals.ui.txtPrice.editingFinished.connect(Products.checkPrice)

        # --- 5. BOTONES (SAVE, MODIFY, DELETE, CLEAN) ---
        # Clientes
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnBuscacli.clicked.connect(Customers.buscaCli)
        globals.ui.btnSavecli.clicked.connect(Customers.saveCli)
        globals.ui.btnModifcli.clicked.connect(Customers.modifcli)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        globals.ui.btnCleancli.clicked.connect(Customers.cleanCli)

        # Productos
        globals.ui.btnSavePro.clicked.connect(Products.savePro)
        globals.ui.btnModifPro.clicked.connect(Products.modifPro)
        globals.ui.btnDelPro.clicked.connect(Products.delPro)

        # Facturación
        globals.ui.btnSaveFac.clicked.connect(Invoice.saveInvoice)
        globals.ui.btnOk.clicked.connect(Invoice.saveSales)  # El tick azul
        globals.ui.btnCleancli_4.clicked.connect(Invoice.cleanFac)  # El botón de limpiar/imprimir

        # Si creaste el botón específico de imprimir en QtDesigner:
        if hasattr(globals.ui, 'btnPrintFac'):
            globals.ui.btnPrintFac.clicked.connect(Invoice.reportFactura)

        # --- 6. EVENTOS DE TABLAS Y COMBOS ---
        globals.ui.tableCustomerlist.clicked.connect(Customers.selectCustomer)
        globals.ui.tableProducts.clicked.connect(Products.selectProduct)
        globals.ui.tableFac.clicked.connect(Invoice.selectInvoice)
        globals.ui.tableSales.itemChanged.connect(Invoice.cellChangedSales)
        globals.ui.cmbProvcli.currentIndexChanged.connect(Events.loadMunicli)
        globals.ui.chkHistoricocli.stateChanged.connect(Customers.Historicocli)

        # Mensajes de ayuda (Tooltips)
        self.setTooltips()

    # --- MÉTODOS DE LA CLASE MAIN ---

    def setTooltips(self):
        """Añade mensajes flotantes al pasar el ratón."""
        globals.ui.btnSavecli.setToolTip("Guardar nuevo cliente")
        globals.ui.btnDelcli.setToolTip("Dar de baja al cliente")
        globals.ui.btnCleancli.setToolTip("Limpiar formulario y desbloquear DNI")
        globals.ui.btnOk.setToolTip("Guardar productos y descontar stock")
        globals.ui.btnCleancli_4.setToolTip("Resetear factura y filtros")

    def elegirProvincia(self):
        """Muestra un selector de provincias para generar el report."""
        try:
            lista_provincias = conexion.Conexion.listProv()
            prov, ok = QtWidgets.QInputDialog.getItem(self, "Reporte por Provincia",
                                                      "Seleccione provincia:", lista_provincias, 0, False)
            if ok and prov:
                self.report.reportCliProv(prov)
        except Exception as e:
            print("Error selector provincia:", e)

    def closeEvent(self, event):
        """Captura la 'X' de la ventana para confirmar salida."""
        if Events.messageExit():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())