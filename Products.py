
import globals
from PyQt6 import QtCore, QtWidgets, QtGui
from conexion import *
from events import *

class Products :
    @staticmethod
    def loadTablePro(self=None):
        try:
            # 1. Obtener los datos más recientes de la base de datos
            listTabProducts = Conexion.listProducts()

            # 2. LIMPIEZA TOTAL: Si no haces esto, los datos viejos se quedan debajo
            globals.ui.tableProducts.setRowCount(0)

            # 3. Rellenar fila a fila con los datos nuevos
            for index, record in enumerate(listTabProducts):
                # record según la query de conexion.py: [0:Code, 1:Name, 2:Family, 3:Stock, 4:Price]
                globals.ui.tableProducts.insertRow(index)

                # Nombre (Columna 0 de tu tabla UI)
                globals.ui.tableProducts.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[1])))

                # Stock (Columna 1 de tu tabla UI)
                stock_valor = str(record[3])
                stock_item = QtWidgets.QTableWidgetItem(stock_valor)
                if stock_valor.isdigit() and int(stock_valor) <= 5:
                    stock_item.setBackground(QtGui.QColor(255, 200, 200))  # Color rojo si hay poco
                globals.ui.tableProducts.setItem(index, 1, stock_item)

                # Familia (Columna 2 de tu tabla UI)
                globals.ui.tableProducts.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))

                # Precio (Columna 3 de tu tabla UI)
                globals.ui.tableProducts.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[4]) + " €"))

                # Alineación estética
                globals.ui.tableProducts.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tableProducts.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        except Exception as error:
            print("Error en loadTablePro visual:", error)

    @staticmethod
    def selectProduct(self=None):
        try:
            row = globals.ui.tableProducts.selectedItems()
            if not row: return

            # En tu tabla la columna 0 es el nombre
            nombre_pro = row[0].text()
            record = Conexion.dataOneProduct(nombre_pro)

            if record:
                # record es: [0:Code, 1:Name, 2:Family, 3:Stock, 4:Price]
                globals.ui.txtCode.setText(str(record[0]))
                globals.ui.txtName.setText(str(record[1]))
                globals.ui.cmbFamily.setCurrentText(str(record[2]))
                globals.ui.txtStock.setText(str(record[3]))
                globals.ui.txtPrice.setText(str(record[4]))

        except Exception as error:
            print("Error en selectProduct ", error)

    @staticmethod
    def delPro():
        try:
            codigo = globals.ui.txtCode.text()
            if not codigo:
                QtWidgets.QMessageBox.warning(None, "Aviso", "Selecciona un producto de la tabla")
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Aviso")
            mbox.setText(f"¿Desea eliminar el producto con código {codigo}?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                if Conexion.deletePro(codigo):
                    QtWidgets.QMessageBox.information(None, "Éxito", "Producto eliminado")
                    # CORRECCIÓN: Llamamos a Products, no a Customers
                    Products.loadTablePro(True)
                    # Limpiar campos
                    for w in [globals.ui.txtCode, globals.ui.txtName, globals.ui.txtStock, globals.ui.txtPrice]:
                        w.setText("")
                else:
                    QtWidgets.QMessageBox.critical(None, "Error", "No se pudo eliminar")
        except Exception as error:
            print("error delete Product ", error)

    @staticmethod
    def savePro(self):
        try:
            # CORRECCIÓN: cmbFamily usa currentText()
            newpro = [
                globals.ui.txtCode.text(),
                globals.ui.txtName.text(),
                globals.ui.cmbFamily.currentText(),  # Antes era .text()
                globals.ui.txtStock.text(),
                globals.ui.txtPrice.text()
            ]

            # Validar que los campos no estén vacíos
            if all(newpro):
                if Conexion.addPro(newpro):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Información")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Producto añadido correctamente")
                    mbox.exec()
                    Products.loadTablePro(True)  # Recargar tabla
                else:
                    QtWidgets.QMessageBox.warning(None, "Aviso", "El código ya existe o error en base de datos")
            else:
                QtWidgets.QMessageBox.warning(None, "Aviso", "Faltan datos por rellenar")

        except Exception as error:
            print("error en savePro ", error)

    @staticmethod
    def modifPro():
        try:
            # 1. Recogemos los datos de la interfaz
            codigo = globals.ui.txtCode.text()
            nombre = globals.ui.txtName.text()
            familia = globals.ui.cmbFamily.currentText()
            stock = globals.ui.txtStock.text()
            precio = globals.ui.txtPrice.text()

            # 2. Verificamos que haya un código (que se haya seleccionado algo)
            if codigo == "":
                QtWidgets.QMessageBox.warning(None, "Aviso", "Seleccione un producto de la tabla")
                return

            datosPro = [codigo, nombre, familia, stock, precio]

            # 3. Llamada a la base de datos
            if Conexion.modifPro(datosPro):
                QtWidgets.QMessageBox.information(None, "Éxito", "Producto modificado correctamente")
                # 4. Refrescamos la tabla para que se vea el cambio
                Products.loadTablePro()
            else:
                QtWidgets.QMessageBox.warning(None, "Error", "No se pudo modificar el producto")

        except Exception as error:
            print("Error en modifPro (Products.py):", error)

    @staticmethod
    def checkPrice():
        """ Valida que el precio sea numérico y positivo """
        try:
            precio = globals.ui.txtPrice.text().replace(',', '.')
            if float(precio) > 0:
                globals.ui.txtPrice.setText(f"{float(precio):.2f}")
                globals.ui.txtPrice.setStyleSheet("background-color: white;")
            else:
                raise ValueError
        except:
            globals.ui.txtPrice.setText("")
            globals.ui.txtPrice.setPlaceholderText("0.00")
            globals.ui.txtPrice.setStyleSheet("background-color: #FFC0CB;")

