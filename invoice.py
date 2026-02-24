import conexion
import globals
from PyQt6 import QtWidgets, QtCore, QtGui
from datetime import datetime


class Invoice():

    @staticmethod
    def cleanFac():
        """
        MÉTODO: Limpiar Interfaz de Facturación.
        QUÉ HACE: Resetea campos de texto, labels del cliente y limpia la tabla de ventas.
        PARA EL EXAMEN: Es el botón de la flecha circular. Quita los filtros y vuelve a mostrar todas las facturas.
        """
        try:
            # 1. Limpiar cabecera de factura
            globals.ui.lblNumFac.setText("")
            globals.ui.txtDnifac.setText("")
            globals.ui.lblFechaFac.setText("")

            # 2. Limpiar labels informativos del cliente (derecha)
            globals.ui.lblNameInv.setText("")
            globals.ui.lblInvoiceTypeInv.setText("")
            globals.ui.lblAddressInv.setText("")
            globals.ui.lblMobileInv.setText("")
            globals.ui.lblStatusInv.setText("")

            # 3. Limpiar tabla de productos y totales
            globals.ui.tableSales.setRowCount(0)
            globals.ui.lblSubTotalInv.setText("0.00 €")
            globals.ui.lblIVAInv.setText("0.00 €")
            globals.ui.lblTotalInv.setText("0.00 €")

            # 4. Recargar todas las facturas y preparar fila nueva para escribir
            Invoice.loadTablefac()
            Invoice.activeSales(0)

        except Exception as error:
            print("Error en cleanFac:", error)

    @staticmethod
    def buscaCli():
        """
        MÉTODO: Cargar datos del cliente en Facturación.
        QUÉ HACE: Al poner un DNI, rellena los labels de la derecha.
        """
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            if dni == "": dni = "00000000T"
            globals.ui.txtDnifac.setText(dni)
            record = conexion.Conexion.dataOneCustomer(dni)
            if record:
                globals.ui.lblNameInv.setText(f"{record[2]}, {record[3]}")
                globals.ui.lblInvoiceTypeInv.setText(str(record[9]))
                globals.ui.lblAddressInv.setText(str(record[6]))
                globals.ui.lblMobileInv.setText(str(record[5]))
                globals.ui.lblStatusInv.setText("Activo" if str(record[10]) == "True" else "Inactivo")
            else:
                Invoice.cleanFac()
        except Exception as error:
            print("Error buscaCli:", error)

    @staticmethod
    def saveInvoice():
        """
        MÉTODO: Guardar Cabecera de Factura.
        QUÉ HACE: Crea el registro en la tabla 'invoices'. No imprime.
        """
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            fecha = datetime.now().strftime("%d/%m/%Y")
            if dni == "":
                QtWidgets.QMessageBox.warning(None, "Aviso", "Falta el DNI del cliente")
                return
            if conexion.Conexion.insertInvoice(dni, fecha):
                Invoice.loadTablefac()
                QtWidgets.QMessageBox.information(None, "Éxito", "Factura creada. Añade los productos.")
        except Exception as e:
            print("Error saveInvoice:", e)

    @staticmethod
    def loadTablefac(dni=None):
        """
        MÉTODO: Cargar lista de facturas (Izquierda).
        QUÉ HACE: Muestra las facturas y configura las columnas para que se vea la papelera.
        """
        try:
            header = globals.ui.tableFac.horizontalHeader()
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tableFac.setColumnWidth(3, 40)

            records = conexion.Conexion.allInvoices(dni)
            globals.ui.tableFac.setRowCount(0)
            for index, record in enumerate(records):
                globals.ui.tableFac.insertRow(index)
                globals.ui.tableFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tableFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tableFac.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))

                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QtGui.QIcon("./img/basura.png"))
                btn_del.setFixedSize(24, 24)
                btn_del.setStyleSheet("background-color: transparent; border: none;")
                # Papelera de factura guardada -> Alerta
                btn_del.clicked.connect(lambda checked, idf=record[0]: Invoice.borrarFactura(idf))
                globals.ui.tableFac.setCellWidget(index, 3, btn_del)
                for i in range(3): globals.ui.tableFac.item(index, i).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            print("Error loadTablefac:", e)

    @staticmethod
    def selectInvoice():
        """ MÉTODO: Seleccionar factura de la tabla para ver sus productos. """
        try:
            row = globals.ui.tableFac.selectedItems()
            if not row: return
            id_fac = row[0].text()
            globals.ui.lblNumFac.setText(id_fac)
            globals.ui.txtDnifac.setText(row[1].text())
            globals.ui.lblFechaFac.setText(row[2].text())
            Invoice.buscaCli()
            ventas = conexion.Conexion.getVentas(id_fac)
            Invoice.loadTablasales(ventas)
        except Exception as error:
            print("Error selectInvoice:", error)

    @staticmethod
    def activeSales(row):
        """ MÉTODO: Crear fila vacía en la tabla de ventas. """
        try:
            if globals.ui.tableSales.rowCount() <= row:
                globals.ui.tableSales.setRowCount(row + 1)
            for col in range(5):
                item = QtWidgets.QTableWidgetItem("")
                if col in [2, 4]:  # Nombre y Total no se editan
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
                globals.ui.tableSales.setItem(row, col, item)
        except Exception as e:
            print(e)

    @staticmethod
    def cellChangedSales(item):
        """ MÉTODO: Autocompletar producto y calcular línea al escribir. """
        row, col = item.row(), item.column()
        if row < 0: return
        value = item.text().strip()
        if value == "": return

        globals.ui.tableSales.blockSignals(True)
        try:
            if col == 0:  # Escribe Código
                datos = conexion.Conexion.selectProduct(value)
                if datos:
                    globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(datos[0])))
                    globals.ui.tableSales.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{datos[1]:.2f}"))
                else:
                    item.setText("")
            elif col == 1:  # Escribe Cantidad
                try:
                    precio = float(globals.ui.tableSales.item(row, 3).text())
                    total = round(float(value) * precio, 2)
                    globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(total)))
                    if row == globals.ui.tableSales.rowCount() - 1:
                        Invoice.activeSales(row + 1)  # Uno por uno
                    Invoice.calculateTotals()
                except:
                    pass
        finally:
            globals.ui.tableSales.blockSignals(False)

    @staticmethod
    def saveSales():
        """
        MÉTODO: Guardar Productos (Check Azul).
        QUÉ HACE: Valida Stock ("Solo quedan X") y descuenta del almacén.
        """
        try:
            id_fac = globals.ui.lblNumFac.text()
            if id_fac == "": return
            for i in range(globals.ui.tableSales.rowCount()):
                item_id = globals.ui.tableSales.item(i, 0)
                item_qty = globals.ui.tableSales.item(i, 1)
                if item_id and item_id.text() != "" and item_qty and item_qty.text() != "":
                    btn = globals.ui.tableSales.cellWidget(i, 5)
                    if btn and btn.isEnabled() == False: continue  # Ya guardado

                    codigo = item_id.text()
                    cantidad = int(item_qty.text())
                    prod = conexion.Conexion.dataOneProduct_by_Code(codigo)

                    if prod and cantidad > int(prod[3]):
                        QtWidgets.QMessageBox.warning(None, "Stock", f"Solo quedan {prod[3]} unidades de {prod[1]}.")
                        return

                    if conexion.Conexion.insertVenta([id_fac, codigo, cantidad]):
                        conexion.Conexion.updateStock(codigo, cantidad)

            Invoice.loadTablasales(conexion.Conexion.getVentas(id_fac))
            from Products import Products
            Products.loadTablePro()
        except Exception as e:
            print(e)

    @staticmethod
    def loadTablasales(records):
        """ MÉTODO: Rellenar la tabla de ventas con los datos de la BD. """
        try:
            header = globals.ui.tableSales.horizontalHeader()
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)  # Producto estirable
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tableSales.setColumnWidth(5, 35)

            globals.ui.tableSales.setRowCount(0)
            for index, row in enumerate(records):
                globals.ui.tableSales.insertRow(index)
                globals.ui.tableSales.setItem(index, 0, QtWidgets.QTableWidgetItem(str(row[1])))  # Cod
                globals.ui.tableSales.setItem(index, 1, QtWidgets.QTableWidgetItem(str(row[4])))  # Cant
                globals.ui.tableSales.setItem(index, 2, QtWidgets.QTableWidgetItem(str(row[2])))  # Nome
                globals.ui.tableSales.setItem(index, 3, QtWidgets.QTableWidgetItem(str(row[3])))  # Precio
                globals.ui.tableSales.setItem(index, 4, QtWidgets.QTableWidgetItem(str(row[5])))  # Total

                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QtGui.QIcon("./img/basura.png"))
                btn_del.setFixedSize(22, 22)
                btn_del.setStyleSheet("background-color: transparent; border: none;")
                # Si ya está en la BD, la papelera solo avisa
                btn_del.clicked.connect(lambda: QtWidgets.QMessageBox.warning(None, "Aviso", "Producto ya facturado."))
                globals.ui.tableSales.setCellWidget(index, 5, btn_del)

            Invoice.calculateTotals()
            Invoice.activeSales(globals.ui.tableSales.rowCount())
        except Exception as e:
            print(e)

    @staticmethod
    def borrarFactura(id_factura):
        """ MÉTODO: Bloqueo de borrado de facturas guardadas. """
        QtWidgets.QMessageBox.critical(None, "Error", "No se pueden eliminar facturas que ya han sido guardadas.")

    @staticmethod
    def calculateTotals():
        """ MÉTODO: Calcular Subtotal, IVA y Total. """
        subtotal = 0.0
        for i in range(globals.ui.tableSales.rowCount()):
            item = globals.ui.tableSales.item(i, 4)
            if item and item.text(): subtotal += float(item.text())
        globals.ui.lblSubTotalInv.setText(f"{subtotal:.2f} €")
        globals.ui.lblIVAInv.setText(f"{subtotal * 0.21:.2f} €")
        globals.ui.lblTotalInv.setText(f"{subtotal * 1.21:.2f} €")

    @staticmethod
    def reportFactura():
        """ MÉTODO: Imprimir Factura. """
        if globals.ui.lblNumFac.text():
            from reports import Reports
            Reports().ticket()
        else:
            QtWidgets.QMessageBox.warning(None, "Aviso", "Selecciona una factura")