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
                QtWidgets.QMessageBox.warning(None, "Aviso", "Debe introducir un DNI")
                return

            if conexion.Conexion.insertInvoice(dni, fecha):
                Invoice.loadTablefac()
                QtWidgets.QMessageBox.information(None, "Éxito", "Factura guardada")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "No se pudo guardar la factura.")
        except Exception as e:
            print("Error en saveInvoice:", e)

    @staticmethod
    def loadTablefac():
        try:
            header = globals.ui.tableFac.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tableFac.setColumnWidth(3, 30)

            records = conexion.Conexion.allInvoices()
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

                id_factura = record[0]
                btn_del.clicked.connect(lambda checked, idf=id_factura: Invoice.borrarFactura(idf))
                globals.ui.tableFac.setCellWidget(index, 3, btn_del)

                for j in range(3):
                    globals.ui.tableFac.item(index, j).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            if records:
                datos = records[0]
                globals.ui.lblNumFac.setText(str(datos[0]))
                globals.ui.txtDnifac.setText(str(datos[1]))
                globals.ui.lblFechaFac.setText(str(datos[2]))
                Invoice.buscaCli()
        except Exception as error:
            print("error load tablafac", error)

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
        value = item.text().strip()

        if value == "": return

        globals.ui.tableSales.blockSignals(True)
        try:
            # Col 0: Código Producto
            if col == 0:
                datos = conexion.Conexion.selectProduct(value)
                if datos:
                    # En tu tabla: 2 es Product Name, 3 es Unit Price
                    globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(datos[0])))
                    globals.ui.tableSales.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{datos[1]:.2f}"))
                else:
                    QtWidgets.QMessageBox.warning(None, "Error", "Producto no existe")
                    item.setText("")

            # Col 1: Cantidad (Amount)
            elif col == 1:
                try:
                    cantidad = float(value)
                    precio_texto = globals.ui.tableSales.item(row, 3).text()
                    if precio_texto:
                        precio = float(precio_texto)
                        total_linea = round(cantidad * precio, 2)
                        globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(total_linea)))

                        # Si es la última fila, añadir nueva
                        if row == globals.ui.tableSales.rowCount() - 1:
                            Invoice.activeSales(row + 1)
                        Invoice.calculateTotals()
                except ValueError:
                    item.setText("")
        finally:
            globals.ui.tableSales.blockSignals(False)

    @staticmethod
    def loadTablasales(records):
        try:
            globals.ui.tableSales.setRowCount(0)
            for index, row in enumerate(records):
                globals.ui.tableSales.insertRow(index)
                # record JOIN: [idv, idpro, nombre, precio, cantidad, total]
                globals.ui.tableSales.setItem(index, 0, QtWidgets.QTableWidgetItem(str(row[1])))  # ID
                globals.ui.tableSales.setItem(index, 1, QtWidgets.QTableWidgetItem(str(row[4])))  # Cantidad
                globals.ui.tableSales.setItem(index, 2, QtWidgets.QTableWidgetItem(str(row[2])))  # Nombre
                globals.ui.tableSales.setItem(index, 3, QtWidgets.QTableWidgetItem(str(row[3])))  # Precio
                globals.ui.tableSales.setItem(index, 4, QtWidgets.QTableWidgetItem(str(row[5])))  # Total
            Invoice.calculateTotals()
            Invoice.activeSales(globals.ui.tableSales.rowCount())
        except Exception as e:
            print("Error loadTablasales:", e)

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
            if not id_fac:
                QtWidgets.QMessageBox.warning(None, "Error", "Selecciona una factura")
                return

            for i in range(globals.ui.tableSales.rowCount()):
                item_id = globals.ui.tableSales.item(i, 0)
                item_qty = globals.ui.tableSales.item(i, 1)
                item_total = globals.ui.tableSales.item(i, 4)

                if item_id and item_id.text() != "" and item_qty and item_qty.text() != "":
                    venta = [id_fac, item_id.text(), item_qty.text(), item_total.text()]
                    if conexion.Conexion.insertVenta(venta):
                        conexion.Conexion.updateStock(item_id.text(), item_qty.text())

            QtWidgets.QMessageBox.information(None, "Éxito", "Venta guardada correctamente")
            from Products import Products
            Products.loadTablePro()
        except Exception as e:
            print("Error saveSales:", e)

    @staticmethod
    def borrarFactura(id_factura):
        try:
            if conexion.Conexion.deleteInvoice(id_factura):
                Invoice.loadTablefac()
                if globals.ui.lblNumFac.text() == str(id_factura):
                    Invoice.cleanFac()
        except Exception as e:
            print("Error borrarFactura:", e)