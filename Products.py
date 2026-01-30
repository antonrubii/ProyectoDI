
import globals
from PyQt6 import QtCore, QtWidgets, QtGui
from conexion import *
from events import *

class Products :
    @staticmethod
    def loadTablePro(varPro):
        try:
            listTabProducts = Conexion.listProducts()
            index = 0
            globals.ui.tableProducts.setRowCount(0)
            for record in listTabProducts:
                globals.ui.tableProducts.insertRow(index)
                globals.ui.tableProducts.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tableProducts.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))

                # COLOR ROJO SI STOCK <= 5 (Como tu compañero)
                stock_item = QtWidgets.QTableWidgetItem(str(record[2]))
                if int(record[2]) <= 5:
                    stock_item.setBackground(QtGui.QColor(255, 200, 200))

                globals.ui.tableProducts.setItem(index, 2, stock_item)
                globals.ui.tableProducts.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[4]) + " €"))
                index += 1
        except Exception as error:
            print("error en loadTablePro ", error)
    @staticmethod
    def selectProduct():
        try:
            row     = globals.ui.tableProducts.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneProduct(str(data[2]))
            print(record)
            boxes = [
                globals.ui.txtCode, globals.ui.txtName, globals.ui.cmbFamily ,
                globals.ui.txtStock, globals.ui.txtPrice
            ]

            for i in range(len(boxes)):
                boxes[i].setText(record[i])

            globals.ui.cmbProvcli.setCurrentText(record[7])
            globals.ui.cmbMunicli.setCurrentText(record[8])

            if str(record[9]) == "paper":
                globals.ui.rbtFacpaper.setChecked(True)
            else:
                globals.ui.rbtFacmail.setChecked(True)
            globals.estado = str(record[10])
            globals.ui.txtDnicli.setEnabled(False)
            globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 200);')


        except Exception as error:
            print("error en selectCustomer ", error)

    @staticmethod
    def delPro():
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Product?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec():
                dni = globals.ui.txtDnicli.text()
                if Conexion.deleteCli(dni):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client deleted")
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Something went wrong, contact the administrator")

                Customers.loadTablePro(True)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Operation cancelled.")
        except Exception as error:
            print("error delete Product ", error)

    @staticmethod
    def savePro(self):
        try:
            newpro = [
                globals.ui.txtCode.text(), globals.ui.txtName.text(), globals.ui.cmbFamily.text(),
                globals.ui.txtStock.text(), globals.ui.txtPrice.text()
            ]

            if globals.ui.rbtFacpaper.isChecked():
                fact = "paper"
            elif globals.ui.rbtFacmail.isChecked():
                fact = "electronic"
            else:
                fact = ""

            newpro.append(fact)

            if Conexion.addCli(newpro) and len(newpro) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Product added successfully")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("WARNING")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Code or Name exists, or data unfilled.\nContact administrator or try again later.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                mbox.exec()

                Products.loadTablePro(True)

        except Exception as error:
            print("error en savePro ", error)

    @staticmethod
    def modifPro():
        try:
            print(globals.estado)
            if globals.estado == str("False"):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Product non activated .Do you want activate?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                if mbox.exec():
                    globals.estado = str("True")
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify Data")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setText("Are you sure modify data?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No )
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            if mbox.exec():
                dni = globals.ui.txtDnicli.text()
                modifPro = [
                    globals.ui.txtCode.text(), globals.ui.txtName.text(), globals.ui.cmbFamily.text(),
                    globals.ui.txtStock.text(), globals.ui.txtPrice.text()
                ]


                if Conexion.modifPro(dni , modifPro):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Cliente modified successfully")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                    if mbox.exec():
                        mbox.hide()
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Warning")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setText("Operation cancelled.")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                        if  mbox.exec():
                            mbox.hide()
                        else:
                            mbox.hide()

        except Exception as error:
            print("error modify client", error)

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

