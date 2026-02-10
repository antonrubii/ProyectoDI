import conexion
import globals
from PyQt6 import QtWidgets, QtCore, QtGui
from datetime import datetime


class Invoice():
    @staticmethod
    def buscaCli():
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            if dni == "": dni = "00000000T"
            globals.ui.txtDnifac.setText(dni)

            record = conexion.Conexion.dataOneCustomer(dni)
            if record:
                # Nombres de etiquetas según tu window.py (lblNameInv, etc.)
                globals.ui.lblNameInv.setText(f"{record[2]}, {record[3]}")
                globals.ui.lblInvoiceTypeInv.setText(str(record[9]))
                globals.ui.lblAddressInv.setText(str(record[6]))
                globals.ui.lblMobileInv.setText(str(record[5]))
                globals.ui.lblStatusInv.setText("Activo" if str(record[10]) == "True" else "Inactivo")
            else:
                Invoice.cleanFac()
        except Exception as error:
            print("error buscaCli factura", error)

    @staticmethod
    def cleanFac():
        try:
            # CORRECCIÓN DE NOMBRES (F mayúscula)
            globals.ui.lblNumFac.setText("")
            globals.ui.txtDnifac.setText("")
            globals.ui.lblFechaFac.setText("")
            globals.ui.lblNameInv.setText("")
            globals.ui.lblInvoiceTypeInv.setText("")
            globals.ui.lblAddressInv.setText("")
            globals.ui.lblMobileInv.setText("")
            globals.ui.lblStatusInv.setText("")
            globals.ui.tableSales.setRowCount(0)
            globals.ui.lblSubTotalInv.setText("0.00")
            globals.ui.lblIVAInv.setText("0.00")
            globals.ui.lblTotalInv.setText("0.00")
            Invoice.activeSales(0)
        except Exception as error:
            print("error limpiar factura", error)

    @staticmethod
    def saveInvoice():
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            fecha = datetime.now().strftime("%d/%m/%Y")
            if dni == "":
                QtWidgets.QMessageBox.warning(None, "Aviso", "Falta el DNI del cliente")
                return

            if conexion.Conexion.insertInvoice(dni, fecha):
                Invoice.loadTablefac()  # Recarga la tabla de la izquierda
                QtWidgets.QMessageBox.information(None, "Éxito", "Factura registrada. Añade los productos abajo.")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "No se pudo crear la factura")
        except Exception as e:
            print("Error saveInvoice:", e)

    @staticmethod
    def loadTablefac():
        try:
            # Configurar anchos para que la papelera se vea siempre
            header = globals.ui.tableFac.horizontalHeader()
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tableFac.setColumnWidth(3, 45)

            records = conexion.Conexion.allInvoices()
            globals.ui.tableFac.setRowCount(0)
            for index, record in enumerate(records):
                globals.ui.tableFac.insertRow(index)
                globals.ui.tableFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tableFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tableFac.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))

                # BOTÓN PAPELERA FACTURA (FUNCIONAL)
                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QtGui.QIcon("./img/basura.png"))
                btn_del.setFixedSize(30, 28)
                btn_del.setStyleSheet("background-color: #FF3B30; border-radius: 4px;")

                # Conectamos al métodode borrar factura pasándole el ID
                id_fac = record[0]
                btn_del.clicked.connect(lambda checked, idf=id_fac: Invoice.borrarFactura(idf))

                globals.ui.tableFac.setCellWidget(index, 3, btn_del)
        except Exception as e:
            print(e)
    @staticmethod
    def selectInvoice():
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
            print("error select invoice", error)

    @staticmethod
    def activeSales(row):
        try:
            globals.ui.tableSales.setRowCount(row + 1)
            for col in range(5):
                item = QtWidgets.QTableWidgetItem("")
                # Columnas 2 (Nombre), 3 (Precio) y 4 (Total) no editables
                if col in [2, 3, 4]:
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setFlags(
                        QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable)
                globals.ui.tableSales.setItem(row, col, item)
                globals.ui.tableSales.item(row, col).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        except Exception as error:
            print("error active sales", error)

    @staticmethod
    def cellChangedSales(item):
        row = item.row()
        col = item.column()
        # Si el cambio es en una fila vieja (no la última), no hacemos nada
        if row < globals.ui.tableSales.rowCount() - 1 and col == 0:
            return

        value = item.text().strip()
        if value == "": return

        globals.ui.tableSales.blockSignals(True)
        try:
            if col == 0:  # Código Producto
                datos = conexion.Conexion.selectProduct(value)
                if datos:
                    globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(datos[0])))
                    globals.ui.tableSales.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{datos[1]:.2f}"))
                else:
                    item.setText("")

            elif col == 1:  # Cantidad
                try:
                    cant = float(value)
                    precio = float(globals.ui.tableSales.item(row, 3).text())
                    total = round(cant * precio, 2)
                    globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(total)))

                    # LOGICA UNO POR UNO: Solo si la fila actual está completa, abrimos la siguiente
                    id_pro = globals.ui.tableSales.item(row, 0).text()
                    if id_pro != "":
                        Invoice.activeSales(row + 1)

                    Invoice.calculateTotals()
                except:
                    item.setText("")
        finally:
            globals.ui.tableSales.blockSignals(False)

    @staticmethod
    def loadTablasales(records):
        try:
            # Configurar anchos para que la papelera se vea siempre
            header = globals.ui.tableSales.horizontalHeader()
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tableSales.setColumnWidth(5, 45)

            globals.ui.tableSales.setRowCount(0)
            for index, row in enumerate(records):
                globals.ui.tableSales.insertRow(index)
                globals.ui.tableSales.setItem(index, 0, QtWidgets.QTableWidgetItem(str(row[1])))  # ID Prod
                globals.ui.tableSales.setItem(index, 1, QtWidgets.QTableWidgetItem(str(row[4])))  # Cant
                globals.ui.tableSales.setItem(index, 2, QtWidgets.QTableWidgetItem(str(row[2])))  # Nombre
                globals.ui.tableSales.setItem(index, 3, QtWidgets.QTableWidgetItem(str(row[3])))  # Precio
                globals.ui.tableSales.setItem(index, 4, QtWidgets.QTableWidgetItem(str(row[5])))  # Total

                # BOTÓN PAPELERA PRODUCTO (FUNCIONAL)
                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QtGui.QIcon("./img/basura.png"))
                btn_del.setFixedSize(28, 24)
                btn_del.setStyleSheet("background-color: #FF3B30; border-radius: 4px;")

                # idv es el ID único de esa línea de venta
                id_venta = row[0]
                btn_del.clicked.connect(lambda checked, idv=id_venta: Invoice.borrarLineaVenta(idv))

                globals.ui.tableSales.setCellWidget(index, 5, btn_del)

            Invoice.calculateTotals()
            Invoice.activeSales(globals.ui.tableSales.rowCount())
        except Exception as e:
            print(e)

    @staticmethod
    def calculateTotals():
        try:
            subtotal = 0.0
            for i in range(globals.ui.tableSales.rowCount()):
                item = globals.ui.tableSales.item(i, 4)
                if item and item.text():
                    subtotal += float(item.text())

            iva = subtotal * 0.21
            total = subtotal + iva

            globals.ui.lblSubTotalInv.setText(f"{subtotal:.2f} €")
            globals.ui.lblIVAInv.setText(f"{iva:.2f} €")
            globals.ui.lblTotalInv.setText(f"{total:.2f} €")
        except Exception as e:
            print("Error calculateTotals:", e)

    @staticmethod
    def saveSales():
        try:
            id_fac = globals.ui.lblNumFac.text()
            if id_fac == "": return

            for i in range(globals.ui.tableSales.rowCount()):
                item_id = globals.ui.tableSales.item(i, 0)
                item_qty = globals.ui.tableSales.item(i, 1)

                if item_id and item_id.text() != "" and item_qty and item_qty.text() != "":
                    # Ignorar si ya está guardado
                    btn = globals.ui.tableSales.cellWidget(i, 5)
                    # (Lógica para saber si es nuevo: si el botón no tiene la alerta de "ya guardado")

                    codigo = item_id.text()
                    cantidad_pedida = int(item_qty.text())

                    # CONSULTAR STOCK REAL
                    prod = conexion.Conexion.dataOneProduct_by_Code(codigo)
                    if prod:
                        stock_actual = int(prod[3])
                        if cantidad_pedida > stock_actual:
                            # LA ALERTA QUE PIDES:
                            QtWidgets.QMessageBox.warning(None, "Stock Insuficiente",
                                                          f"Solo quedan {stock_actual} unidades de {prod[1]}. No puedes pedir {cantidad_pedida}.")
                            return

                            # GUARDAR SITODO OK
                    if conexion.Conexion.insertVenta([id_fac, codigo, cantidad_pedida]):
                        conexion.Conexion.updateStock(codigo, cantidad_pedida)

            Invoice.loadTablasales(conexion.Conexion.getVentas(id_fac))
            from Products import Products
            Products.loadTablePro()
        except Exception as e:
            print(e)

    @staticmethod
    def borrarFactura(id_factura):
        mbox = QtWidgets.QMessageBox()
        mbox.setWindowTitle("Eliminar Factura")
        mbox.setText(f"¿Estás seguro de eliminar la factura Nº {id_factura}?")
        mbox.setInformativeText("Se borrarán también todos los productos asociados.")
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            if conexion.Conexion.deleteInvoice(id_factura):
                Invoice.loadTablefac()
                Invoice.cleanFac()  # Limpiamos la pantalla
                QtWidgets.QMessageBox.information(None, "Éxito", "Factura eliminada")


    @staticmethod
    def borrarLineaVenta(id_venta):
        # Borrar un producto suelto de la factura
        if conexion.Conexion.deleteVenta(id_venta):
            id_fac = globals.ui.lblNumFac.text()
            # Recargamos las ventas para que desaparezca la fila y se actualice el total
            ventas = conexion.Conexion.getVentas(id_fac)
            Invoice.loadTablasales(ventas)

    @staticmethod
    def reportFactura():
        """Este métod se llama al pulsar el nuevo botón btnPrintFac"""
        id_fac = globals.ui.lblNumFac.text()
        if id_fac != "":
            from reports import Reports
            reporte = Reports()
            reporte.ticket()  # Genera el PDF con los datos de la factura actual
        else:
            QtWidgets.QMessageBox.warning(None, "Aviso", "Selecciona una factura para imprimir")