from docutils.nodes import header

import conexion
import globals
from PyQt6 import QtWidgets, QtCore
from datetime import datetime
from time import sleep

class Invoice():
    @staticmethod
    def buscaCli(self=None):
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            if dni == "":
                dni = "00000000T"
            globals.ui.txtDnifac.setText(dni)
            record = conexion.Conexion.dataOneCustomer(dni)
            if len(record) != 0:
                # CORRECCIÓN DE NOMBRES SEGÚN TU WINDOW.PY:
                globals.ui.lblNameInv.setText(record[2] + '   ' + record[3])
                globals.ui.lblInvoiceTypeInv.setText(record[9])
                globals.ui.lblAddressInv.setText(record[6] + '   ' + record[8] + '   ' + record[7])
                globals.ui.lblMobileInv.setText(record[5])
                if record[10] == "True":
                    globals.ui.lblStatusInv.setText('Activo')
                else:
                    globals.ui.lblStatusInv.setText('Inactivo')
            else:
                globals.ui.txtDnifac.setText("")
                # Si el cliente no existe, limpiamos los labels de la derecha
                globals.ui.lblNameInv.setText("")
                globals.ui.lblInvoiceTypeInv.setText("")
                globals.ui.lblAddressInv.setText("")
                globals.ui.lblMobileInv.setText("")
                globals.ui.lblStatusInv.setText("")

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Customers do not Exist")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
        except Exception as error:
            print("error alta factura", error)

    @staticmethod
    def cleanFac(self = None):
        try:
            globals.ui.lblNumfac.setText("")
            globals.ui.txtDnifac.setText("")
            globals.ui.lblFechafac.setText("")
            globals.ui.lblNamefac.setText("")
            globals.ui.lblTipofac.setText("")
            globals.ui.lblDirfac.setText("")
            globals.ui.lblMobilefac.setText("")
            globals.ui.lblStatusfac.setText("")
        except Exception as error:
            print("error limpiar factura", error)

    @staticmethod
    def saveInvoice(self=None):
        try:
            dni = globals.ui.txtDnifac.text()
            data = datetime.now().strftime("%d/%m/%Y")
            if dni != "" and data != "":
                if conexion.Conexion.insertInvoice(dni, data):
                    Invoice.loadTablefac()
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Invoice")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Invoice created successfully")
                    if mbox.exec():
                        mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing Fields or Data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
        except Exception as error:
            print("error save invoice", error)

    @staticmethod
    def loadTablefac(self=None):
        try:
            records = conexion.Conexion.allInvoices()
            globals.ui.tableFac.setRowCount(0)
            index = 0

            # Solo si hay registros en la base de datos
            if records and len(records) > 0:
                for record in records:
                    globals.ui.tableFac.setRowCount(index + 1)
                    globals.ui.tableFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                    globals.ui.tableFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                    globals.ui.tableFac.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))

                    # Alineación
                    for j in range(3):
                        globals.ui.tableFac.item(index, j).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1

                # CARGAR LOS DATOS DE LA PRIMERA FACTURA EN LOS LABELS
                datos = records[0]
                globals.ui.lblNumFac.setText(str(datos[0]))  # Ojo: en tu UI es lblNumFac (F mayúscula)
                globals.ui.txtDnifac.setText(str(datos[1]))
                globals.ui.lblFechaFac.setText(str(datos[2]))  # Ojo: en tu UI es lblFechaFac (F mayúscula)

                # Ejecutamos buscaCli para que rellene los datos del cliente de esa factura
                Invoice.buscaCli()
            else:
                # Si está vacío, simplemente aseguramos que los campos estén limpios
                globals.ui.lblNumFac.setText("")
                globals.ui.lblFechaFac.setText("")

        except Exception as error:
            print("error load tablafac", error)


        def loadFactFirst(self=None):
            try:
                globals.ui.txtDnifac.setText("00000000T")
                globals.ui.lblNumfac.setText("")
                globals.ui.lblFechafac.setText("")
                Invoice.buscaCli(self=None)
            except Exception as error:
                print("error load fac first", error)

    def selectInvoice(self=None):
        try:
            row = globals.ui.tableFac.selectedItems()
            data = [dato.text() for dato in row]
            globals.ui.lblNumfac.setText(str(data[0]))
            globals.ui.txtDnifac.setText(str(data[1]))
            globals.ui.lblFechafac.setText(str(data[2]))
            globals.ui.tableFac.setStyleSheet("""
                        /* Fila seleccionada */
                        QTableWidget::item:selected {
                            background-color: rgb(255, 255, 202);  /* Color pálido amarillo */
                            color: black;                          /* Color del texto al seleccionar */
                        }
                        """)
            Invoice.buscaCli(self=None)
            Invoice.activeSales(self)
        except Exception as error:
            print("error select invoice", error)

    @staticmethod
    def activeSales(self, row=None):
        try:
            # Si no se pasa fila, añadimos la primera fila
            if row is None:
                row = 0
                globals.ui.tableSales.setRowCount(1)
            else:
                # Si es fila nueva, aumentamos el rowCount
                if row >= globals.ui.tableSales.rowCount():
                    globals.ui.tableSales.setRowCount(row + 1)
            globals.ui.tableSales.setStyleSheet("""
                                   /* Fila seleccionada */
                                   QTableWidget::item:selected {
                                       background-color: rgb(255, 255, 202);  /* Color pálido amarillo */
                                       color: black;                          /* Color del texto al seleccionar */
                                   }
                                   """)

            # Columna 0 (código)
            globals.ui.tableSales.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
            globals.ui.tableSales.item(row, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 2 (price)
            globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))

            # Columna 3 (cantidad)
            globals.ui.tableSales.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
            globals.ui.tableSales.item(row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 4 (total)
            globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(""))

        except Exception as error:
            print("error active sales", error)

    def cellChangedSales(self, item):
        try:
            row = item.row()
            col = item.column()
            if row == 0:
                subtotal = 0
            if col not in (0, 3):
                return

            value = item.text().strip()
            if value == "":
                return

            globals.ui.tableSales.blockSignals(True)

            # Columna 0 entonces buscar producto y rellenar nombre y precio
            if col == 0:
                subtotal = 0.00
                data = conexion.Conexion.selectProduct(value)
                globals.ui.tableSales.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[0])))
                globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1])))
                globals.ui.tableSales.item(row, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 3 → calcular total
            elif col == 3:
                cantidad = float(value)
                precio_item = globals.ui.tableSales.item(row, 2)
                if precio_item:
                    precio = float(precio_item.text())
                    tot = round(precio * cantidad, 2)
                    globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(tot)))
                    globals.ui.tableSales.item(row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight
                                                                        | QtCore.Qt.AlignmentFlag.AlignVCenter)

            globals.ui.tableSales.blockSignals(False)

            # Comprobar si la fila actual está completa y añadir nueva fila
            if all([
                globals.ui.tableSales.item(row, 0) and globals.ui.tableSales.item(row, 0).text().strip(),
                globals.ui.tableSales.item(row, 1) and globals.ui.tableSales.item(row, 1).text().strip(),
                globals.ui.tableSales.item(row, 2) and globals.ui.tableSales.item(row, 2).text().strip(),
                globals.ui.tableSales.item(row, 3) and globals.ui.tableSales.item(row, 3).text().strip(),
                globals.ui.tableSales.item(row, 4) and globals.ui.tableSales.item(row, 4).text().strip()
            ]):
                next_row = globals.ui.tableSales.rowCount()
                Invoice.activeSales(self, row=next_row)
                subtotal = subtotal + tot
                ##iva = round(subtotal * iva, 2)
                ##total = round(subtotal + iva, 2)
                globals.ui.lblSubtotal.setText(str(subtotal))
                ##globals.ui.lblIVA.setText(str(iva))
                ##globals.ui.lblTotal.setText(str(total))



        except Exception as error:
            print("Error en cellChangedSales:", error)
            globals.ui.tableSales.blockSignals(False)

    @staticmethod
    def cellsChanged(item):
        try:
            iva = 0.21
            row = item.row()
            col = item.column()

            # Only react on product ID (2) or amount (5)
            if col not in (1, 4):
                return

            value = item.text().strip()
            if not value:
                return

            globals.ui.tblSales.blockSignals(True)

            # If product ID changed, try to auto-fill name (3) and price (4)
            if col == 1:
                data = Conexion.selectProduct(value)
                if not data:
                    QtWidgets.QMessageBox.critical(None, "Error", "Product not found")
                    globals.ui.tblSales.blockSignals(False)
                    return
                # expected data: (name, price)
                name = data[0]
                price = float(data[1])
                # Set name and price as non-editable items
                name_item = QtWidgets.QTableWidgetItem(str(name))
                name_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                globals.ui.tblSales.setItem(row, 2, name_item)

                price_item = QtWidgets.QTableWidgetItem(f"{price:.2f}")
                price_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                globals.ui.tblSales.setItem(row, 3, price_item)

            # Calculate line total if we have price (4) and amount (5)
            price_item = globals.ui.tblSales.item(row, 3)
            qty_item = globals.ui.tblSales.item(row, 4)

            if price_item and qty_item and price_item.text().strip() and qty_item.text().strip():
                try:
                    price = float(price_item.text())
                    qty = float(qty_item.text())
                except Exception:
                    price = 0.0
                    qty = 0.0

                tot = round(price * qty, 2)
                tot_item = QtWidgets.QTableWidgetItem(f"{tot:.2f}")
                tot_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                globals.ui.tblSales.setItem(row, 5, tot_item)

            # Recompute subtotal across table rows (col 6)
            subtotal = 0.0
            for r in range(globals.ui.tblSales.rowCount()):
                it = globals.ui.tblSales.item(r, 5)
                if it and it.text().strip():
                    try:
                        subtotal += float(it.text())
                    except Exception:
                        pass

            globals.subtotal = subtotal
            globals.ui.lblSubtotal.setText(f"{globals.subtotal:.2f} €")
            globals.ui.lblIva.setText(f"{globals.subtotal * iva:.2f} €")
            total = round(globals.subtotal + (globals.subtotal * iva), 2)
            globals.ui.lblTotal.setText(f"{total:.2f} €")

            # If both product id and qty are filled and this is the last row, append a new editable row
            last_row = globals.ui.tblSales.rowCount() - 1
            current_has_product = globals.ui.tblSales.item(row, 1) and globals.ui.tblSales.item(row, 1).text().strip()
            current_has_qty = globals.ui.tblSales.item(row, 4) and globals.ui.tblSales.item(row, 4).text().strip()

            if row == last_row and current_has_product and current_has_qty:
                record = [globals.ui.lblNumfac.text().strip(), globals.ui.tblSales.item(row, 1).text().strip(),
                          globals.ui.tblSales.item(row, 2).text().strip(),
                          globals.ui.tblSales.item(row, 3).text().strip(),
                          globals.ui.tblSales.item(row, 4).text().strip(),
                          globals.ui.tblSales.item(row, 5).text().strip()]
                globals.linesales.append(record)
                globals.ui.tblSales.setRowCount(last_row + 2)
                # Initialize new row (editable on cols 2 and 5)
                for c in range(6):
                    it = globals.ui.tblSales.item(last_row + 1, c)
                    if it:
                        if c in (1, 4):
                            it.setFlags(
                                QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)

        except Exception as e:
            print("Error en guardar factura", e)
            import traceback
            traceback.print_exc()

        finally:
            globals.ui.tblSales.blockSignals(False)

    @staticmethod
    def loadTablasales(records):
        try:
            subtotal = 0.00
            index = 0
            for record in records:
                globals.ui.tableSales.setRowCount(index + 1)
                globals.ui.tableSales.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tableSales.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tableSales.setItem(index, 2,
                                              QtWidgets.QTableWidgetItem(str(record[4])))
                globals.ui.tableSales.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[5])))
                globals.ui.tableSales.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[6]) + " €"))
                subtotal = round(subtotal + float(record[6]), 2)
                globals.ui.tableSales.item(index, 0).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableSales.item(index, 1).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableSales.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableSales.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableSales.item(index, 4).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignRight.AlignRight)
                index += 1
            globals.ui.lblSubtotal.setText(str(subtotal) + " €")
            iva = round(float(subtotal) * 0.21, 2)
            globals.ui.lblIVA.setText(str(iva) + " €")
            total = round(float(subtotal + iva), 2)
            globals.ui.lblTotal.setText(str(total) + " €")
        except Exception as error:
            print("error en loaTableVentas ", error)

    @staticmethod
    def calculateTotals():
        """ Calcula totales sumando la columna 'Total' de tableSales """
        try:
            subtotal = 0.0
            for i in range(globals.ui.tableSales.rowCount()):
                item = globals.ui.tableSales.item(i, 4)
                if item and item.text():
                    # Quitamos el símbolo € si lo tiene
                    valor = item.text().replace(' €', '').replace(',', '.')
                    subtotal += float(valor)

            iva = subtotal * 0.21
            total = subtotal + iva

            globals.ui.lblSubtotal.setText(f"{subtotal:.2f} €")
            globals.ui.lblIVA.setText(f"{iva:.2f} €")
            globals.ui.lblTotal.setText(f"{total:.2f} €")
        except Exception as e:
            print("Error calculando totales:", e)

    @staticmethod
    def cellChangedSales(item):
        """ Lógica mejorada del compañero para autocompletar productos y calcular línea """
        row = item.row()
        col = item.column()

        # Bloqueamos señales para que no entre en bucle infinito al escribir nosotros
        globals.ui.tableSales.blockSignals(True)

        try:
            if col == 0:  # Se ha escrito un código de producto
                codigo = item.text()
                # Buscamos en BBDD (usa tu método selectProduct de conexion)
                datos_pro = conexion.Conexion.selectProduct(codigo)
                if datos_pro:
                    globals.ui.tableSales.setItem(row, 1, QtWidgets.QTableWidgetItem(str(datos_pro[0])))  # Nombre
                    globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(datos_pro[1])))  # Precio
                else:
                    QtWidgets.QMessageBox.warning(None, "Error", "Producto no existe")

            elif col == 3:  # Se ha escrito una cantidad
                try:
                    cant = float(item.text())
                    precio = float(globals.ui.tableSales.item(row, 2).text())
                    total_linea = round(cant * precio, 2)
                    globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{total_linea:.2f}"))

                    # Si la fila está completa, preparamos la siguiente
                    Invoice.activeSales(None, row + 1)
                    Invoice.calculateTotals()
                except:
                    pass
        finally:
            globals.ui.tableSales.blockSignals(False)

    @staticmethod
    def saveSales():
        try:
            # Obtenemos el ID de la factura que está en el label
            id_factura = globals.ui.lblNumFac.text()

            if id_factura == "":
                QtWidgets.QMessageBox.warning(None, "Error", "Debes crear o seleccionar una factura primero")
                return

            # Recorremos todas las filas de la tabla de ventas
            for i in range(globals.ui.tableSales.rowCount()):
                item_id_pro = globals.ui.tableSales.item(i, 0)  # Columna ID Producto
                item_cant = globals.ui.tableSales.item(i, 3)  # Columna Cantidad

                # Solo guardamos si la fila tiene datos
                if item_id_pro and item_id_pro.text() != "" and item_cant and item_cant.text() != "":
                    venta = [
                        id_factura,
                        item_id_pro.text(),
                        item_cant.text(),
                        globals.ui.tableSales.item(i, 1).text(),  # Nombre del producto
                        globals.ui.tableSales.item(i, 2).text(),  # Precio unitario
                        globals.ui.tableSales.item(i, 4).text()  # Total de la línea
                    ]

                    # Llamamos a los métodos de conexion.py (debes tenerlos creados)
                    if conexion.Conexion.insertVenta(venta):
                        conexion.Conexion.updateStock(venta[1], venta[2])

            QtWidgets.QMessageBox.information(None, "Éxito", "Líneas de venta guardadas correctamente")
            # Actualizamos la tabla de productos para ver el nuevo stock
            Products.loadTablePro(True)

        except Exception as e:
            print("Error en saveSales:", e)