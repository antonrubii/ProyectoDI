
import globals
from PyQt6 import QtCore, QtWidgets, QtGui
from conexion import *
from events import *

class Products :
    @staticmethod
    def loadTablePro(varPro):
        try:
            listTabProducts = Conexion.listProducts()
            globals.ui.tableProducts.setRowCount(0)
            for index, record in enumerate(listTabProducts):
                # record: [0:Code, 1:Name, 2:Family, 3:Stock, 4:Price]
                globals.ui.tableProducts.insertRow(index)
                globals.ui.tableProducts.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tableProducts.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))

                stock_item = QtWidgets.QTableWidgetItem(str(record[3]))
                if str(record[3]).isdigit() and int(record[3]) <= 5:
                    stock_item.setBackground(QtGui.QColor(255, 200, 200))
                globals.ui.tableProducts.setItem(index, 1, stock_item)
                globals.ui.tableProducts.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[4]) + " €"))
        except Exception as error:
            print("error en loadTablePro ", error)

        except Exception as error:
            print("Error en loadTablePro ", error)

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
            # Creamos la lista con los datos actuales de los campos de la pestaña Products
            modif_data = [
                globals.ui.txtCode.text(),
                globals.ui.txtName.text(),
                globals.ui.cmbFamily.currentText(),
                globals.ui.txtStock.text(),
                globals.ui.txtPrice.text()
            ]

            if not modif_data[0]: return

            if Conexion.modifPro(modif_data):
                QtWidgets.QMessageBox.information(None, "Éxito", "Producto modificado")
                Products.loadTablePro(True)
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "Error al modificar")
        except Exception as error:
            print("error modify product", error)

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

