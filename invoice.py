import conexion
import globals
from PyQt6 import QtWidgets, QtCore, QtGui
from datetime import datetime


class Invoice():

    # --- 1. GESTIÓN DEL CLIENTE EN LA FACTURA ---

    @staticmethod
    def buscaCli():
        """
        MÉT0DO: Buscar cliente para factura.
        QUÉ HACE: Al escribir el DNI en la pestaña de facturas, busca sus datos en la BD y rellena los labels informativos (Nombre, Dirección, etc.).
        PARA EL EXAMEN: Si el cliente no existe, limpia los campos y avisa. Se suele conectar al evento 'editingFinished' de txtDnifac.
        """
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            if dni == "": dni = "00000000T"  # DNI genérico por defecto
            globals.ui.txtDnifac.setText(dni)

            record = conexion.Conexion.dataOneCustomer(dni)
            if record:
                # Rellenar labels de la interfaz (según window.py)
                globals.ui.lblNameInv.setText(f"{record[2]}, {record[3]}")
                globals.ui.lblInvoiceTypeInv.setText(str(record[9]))
                globals.ui.lblAddressInv.setText(str(record[6]))
                globals.ui.lblMobileInv.setText(str(record[5]))
                globals.ui.lblStatusInv.setText("Activo" if str(record[10]) == "True" else "Inactivo")
            else:
                Invoice.cleanFac()  # Si no existe, limpiamos t0do
                QtWidgets.QMessageBox.warning(None, "Error", "El cliente no existe.")
        except Exception as error:
            print("Error buscaCli factura:", error)

    # --- 2. GESTIÓN DE LA CABECERA DE FACTURA (Tabla Izquierda) ---

    @staticmethod
    def saveInvoice():
        """
        MÉT0DO: Crear Factura.
        QUÉ HACE: Registra una nueva factura vacía (DNI + Fecha) en la base de datos.
        PARA EL EXAMEN: Es el botón 'Save' azul de arriba. No añade productos, solo crea el 'número' de factura.
        """
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            fecha = datetime.now().strftime("%d/%m/%Y")
            if dni == "":
                QtWidgets.QMessageBox.warning(None, "Aviso", "Falta el DNI del cliente")
                return

            if conexion.Conexion.insertInvoice(dni, fecha):
                Invoice.loadTablefac()  # Recarga la lista de facturas
                QtWidgets.QMessageBox.information(None, "Éxito", "Factura creada. Añade productos a la derecha.")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "No se pudo crear la factura")
        except Exception as e:
            print("Error saveInvoice:", e)

    @staticmethod
    def loadTablefac():
        try:
            # 1. CONFIGURACIÓN DE COLUMNAS (Para que no haya scroll horizontal)
            header = globals.ui.tableFac.horizontalHeader()

            # Col 0 (Nº Fac): Lo justo para el número
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            # Col 1 (DNI): SE ESTIRA para ocupar el hueco (así empuja el resto a la vista)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            # Col 2 (Fecha): Lo justo para la fecha
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            # Col 3 (Papelera): Ancho fijo pequeño
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tableFac.setColumnWidth(3, 35)

            # 2. CARGA DE DATOS
            records = conexion.Conexion.allInvoices()
            globals.ui.tableFac.setRowCount(0)

            for index, record in enumerate(records):
                globals.ui.tableFac.insertRow(index)

                # Rellenar datos
                globals.ui.tableFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))  # ID
                globals.ui.tableFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))  # DNI
                globals.ui.tableFac.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))  # Fecha

                # BOTÓN PAPELERA
                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QtGui.QIcon("./img/basura.png"))
                btn_del.setFixedSize(24, 24)
                btn_del.setStyleSheet("background-color: transparent; border: none; padding: 0px;")

                # Lógica: Alerta si la factura ya existe (no dejar borrar)
                id_fac = record[0]
                btn_del.clicked.connect(lambda checked, idf=id_fac: Invoice.borrarFactura(idf))

                globals.ui.tableFac.setCellWidget(index, 3, btn_del)

                # Alineación centrada para los textos
                for i in range(3):
                    globals.ui.tableFac.item(index, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Ocultar rejilla para look Apple
            globals.ui.tableFac.setShowGrid(False)

        except Exception as e:
            print("Error loadTablefac:", e)

    @staticmethod
    def selectInvoice():
        """
        MÉT0DO: Seleccionar Factura.
        QUÉ HACE: Al pinchar una factura a la izquierda, carga sus datos arriba y sus productos a la derecha.
        """
        try:
            row = globals.ui.tableFac.selectedItems()
            if not row: return
            id_fac = row[0].text()
            globals.ui.lblNumFac.setText(id_fac)
            globals.ui.txtDnifac.setText(row[1].text())
            globals.ui.lblFechaFac.setText(row[2].text())

            Invoice.buscaCli()  # Cargar datos cliente
            ventas = conexion.Conexion.getVentas(id_fac)
            Invoice.loadTablasales(ventas)  # Cargar productos de la factura
        except Exception as error:
            print("Error selectInvoice:", error)

    # --- 3. GESTIÓN DE VENTAS/PRODUCTOS (Tabla Derecha) ---

    @staticmethod
    def loadTablasales(records):
        """
        MÉT0DO: Listar Productos de la Factura.
        QUÉ HACE: Rellena la tabla de ventas con los productos guardados y sus subtotales.
        PARA EL EXAMEN: Configura el 'Stretch' en la columna de Nombre para evitar barras de scroll.
        """
        try:
            header = globals.ui.tableSales.horizontalHeader()
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)  # El nombre se estira
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)  # Papelera fija
            globals.ui.tableSales.setColumnWidth(5, 30)

            globals.ui.tableSales.setRowCount(0)
            for index, row in enumerate(records):
                globals.ui.tableSales.insertRow(index)
                globals.ui.tableSales.setItem(index, 0, QtWidgets.QTableWidgetItem(str(row[1])))  # Cod
                globals.ui.tableSales.setItem(index, 1, QtWidgets.QTableWidgetItem(str(row[4])))  # Cant
                globals.ui.tableSales.setItem(index, 2, QtWidgets.QTableWidgetItem(str(row[2])))  # Nombre
                globals.ui.tableSales.setItem(index, 3, QtWidgets.QTableWidgetItem(str(row[3])))  # Precio
                globals.ui.tableSales.setItem(index, 4, QtWidgets.QTableWidgetItem(str(row[5])))  # Total

                # Botón Borrar Línea de Venta
                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QtGui.QIcon("./img/basura.png"))
                btn_del.setFixedSize(22, 22)
                btn_del.setStyleSheet("background-color: transparent; border: none;")
                btn_del.clicked.connect(lambda checked, idv=row[0]: Invoice.borrarLineaVenta(idv))
                globals.ui.tableSales.setCellWidget(index, 5, btn_del)

            Invoice.calculateTotals()
            Invoice.activeSales(globals.ui.tableSales.rowCount())  # Fila nueva para escribir
        except Exception as e:
            print("Error loadTablasales:", e)

    @staticmethod
    def activeSales(row):
        """
        MÉT0DO: Preparar fila de escritura.
        QUÉ HACE: Añade una fila vacía y hace que las columnas de Nombre y Total no sean editables por el usuario.
        """
        try:
            if globals.ui.tableSales.rowCount() <= row:
                globals.ui.tableSales.setRowCount(row + 1)
            for col in range(5):
                item = QtWidgets.QTableWidgetItem("")
                if col in [2, 4]:  # Nombre y Total son automáticos, no se escriben
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
                globals.ui.tableSales.setItem(row, col, item)
        except Exception as e:
            print(e)

    @staticmethod
    def cellChangedSales(item):
        """
        MÉT0DO: Autocompletado de Venta.
        QUÉ HACE: Al escribir un CÓDIGO (col 0), busca el nombre/precio. Al escribir CANTIDAD (col 1), calcula el total de línea.
        PARA EL EXAMEN: Logra el efecto 'uno por uno': solo abre fila nueva cuando la actual está lista.
        """
        row, col = item.row(), item.column()
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
                    item.setText("")  # Borra si no existe
            elif col == 1:  # Escribe Cantidad
                try:
                    precio = float(globals.ui.tableSales.item(row, 3).text())
                    globals.ui.tableSales.setItem(row, 4,
                                                  QtWidgets.QTableWidgetItem(str(round(float(value) * precio, 2))))
                    if row == globals.ui.tableSales.rowCount() - 1:
                        Invoice.activeSales(row + 1)  # Crear siguiente fila
                    Invoice.calculateTotals()
                except:
                    pass
        finally:
            globals.ui.tableSales.blockSignals(False)

    @staticmethod
    def saveSales():
        """
        MÉT0DO: Confirmar Venta (Check Azul).
        QUÉ HACE: Guarda los productos en la BD y descuenta el STOCK.
        PARA EL EXAMEN: Incluye la ALERTA DE STOCK ("Solo quedan X").
        """
        try:
            id_fac = globals.ui.lblNumFac.text()
            if id_fac == "": return
            for i in range(globals.ui.tableSales.rowCount()):
                item_id = globals.ui.tableSales.item(i, 0)
                item_qty = globals.ui.tableSales.item(i, 1)
                if item_id and item_id.text() != "" and item_qty and item_qty.text() != "":
                    # Verificar si ya está guardado (si tiene papelera activa)
                    btn = globals.ui.tableSales.cellWidget(i, 5)
                    if btn and btn.isEnabled() == False: continue

                    codigo = item_id.text()
                    cantidad = int(item_qty.text())

                    # CONTROL STOCK
                    prod = conexion.Conexion.dataOneProduct_by_Code(codigo)
                    if prod and cantidad > int(prod[3]):
                        QtWidgets.QMessageBox.warning(None, "Stock", f"Solo quedan {prod[3]} unidades.")
                        return

                    if conexion.Conexion.insertVenta([id_fac, codigo, cantidad]):
                        conexion.Conexion.updateStock(codigo, cantidad)

            Invoice.loadTablasales(conexion.Conexion.getVentas(id_fac))
            from Products import Products
            Products.loadTablePro()
        except Exception as e:
            print(e)

    # --- 4. ACCIONES DE BORRADO ---

    @staticmethod
    def borrarFactura(id_factura):
        """ QUÉ HACE: Salta alerta de seguridad para facturas ya guardadas. """
        QtWidgets.QMessageBox.critical(None, "Denegado", "Factura guardada. No se puede eliminar.")

    @staticmethod
    def borrarLineaVenta(id_venta):
        """ QUÉ HACE: Borra un producto de la factura y refresca la vista. """
        if conexion.Conexion.deleteVenta(id_venta):
            id_fac = globals.ui.lblNumFac.text()
            Invoice.loadTablasales(conexion.Conexion.getVentas(id_fac))

    # --- 5. UTILIDADES E INFORMES ---

    @staticmethod
    def calculateTotals():
        """ QUÉ HACE: Suma los subtotales de la tabla y calcula IVA (21%) y Total. """
        subtotal = 0.0
        for i in range(globals.ui.tableSales.rowCount()):
            item = globals.ui.tableSales.item(i, 4)
            if item and item.text(): subtotal += float(item.text())
        globals.ui.lblSubTotalInv.setText(f"{subtotal:.2f} €")
        globals.ui.lblIVAInv.setText(f"{subtotal * 0.21:.2f} €")
        globals.ui.lblTotalInv.setText(f"{subtotal * 1.21:.2f} €")

    @staticmethod
    def cleanFac():
        """ QUÉ HACE: Resetea toda la pestaña de facturación. """
        labels = [globals.ui.lblNumFac, globals.ui.lblFechaFac, globals.ui.lblNameInv,
                  globals.ui.lblInvoiceTypeInv, globals.ui.lblAddressInv, globals.ui.lblMobileInv,
                  globals.ui.lblStatusInv]
        for l in labels: l.setText("")
        globals.ui.txtDnifac.setText("")
        globals.ui.tableSales.setRowCount(0)
        Invoice.calculateTotals()
        Invoice.activeSales(0)

    @staticmethod
    def reportFactura():
        """ QUÉ HACE: Lanza el PDF de la factura actual. Se conecta al botón 'Print'. """
        if globals.ui.lblNumFac.text():
            from reports import Reports
            Reports().ticket()
        else:
            QtWidgets.QMessageBox.warning(None, "Aviso", "Selecciona una factura")