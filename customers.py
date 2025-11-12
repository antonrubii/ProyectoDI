
import globals
from PyQt6 import QtCore, QtWidgets, QtGui
from conexion import *


class Customers:

    def checkDni(self=None):
        try:
            # Evita desconectar si no estaba conectado
            try:
                globals.ui.txtDnicli.editingFinished.disconnect(Customers.checkDni)
            except TypeError:
                pass

            dni = globals.ui.txtDnicli.text()
            dni = str(dni).upper()
            globals.ui.txtDnicli.setText(dni)

            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"

            if len(dni) == 9:
                dig_control = dni[8]
                dni_num = dni[:8]
                if dni_num[0] in dig_ext:
                    dni_num = dni_num.replace(dni_num[0], reemp_dig_ext[dni_num[0]])
                if len(dni_num) == len([n for n in dni_num if n in numeros]) and tabla[
                    int(dni_num) % 23] == dig_control:
                    globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')
                else:
                    globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                    globals.ui.txtDnicli.setText("")
                    globals.ui.txtDnicli.setPlaceholderText("Invalid DNI/NIE")
                    globals.ui.txtDnicli.setFocus()
            else:
                globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtDnicli.setText("")
                globals.ui.txtDnicli.setPlaceholderText("Invalid DNI/NIE")
                globals.ui.txtDnicli.setFocus()

        except Exception as error:
            print("error en validar dni ", error)
        finally:
            globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)

    @staticmethod
    def capitalizar(texto, widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("Error en capitalizar ", error)

    @staticmethod
    def checkMail(email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(patron, email):
            globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtEmailcli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtEmailcli.setText("")
            globals.ui.txtEmailcli.setPlaceholderText("Invalid email")
            globals.ui.txtEmailcli.setFocus()

    @staticmethod
    def checkMobil(numero):
        patron = r'^[67]\d{8}$'
        if re.match(patron, numero):
            globals.ui.txtMobilecli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtMobilecli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtMobilecli.setText("")
            globals.ui.txtMobilecli.setPlaceholderText("Invalid mobile number")
            globals.ui.txtMobilecli.setFocus()

    @staticmethod
    def cleanCli():
        try:
            formcli = [
                globals.ui.txtDnicli, globals.ui.txtEmailcli, globals.ui.txtMobilecli,
                globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNamecli,
                globals.ui.txtDircli
            ]

            for dato in formcli:
                dato.setText("")

            Events.loadProv()
            globals.ui.cmbMunicli.clear()
            globals.ui.rbtFacmail.setChecked(True)
            globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 220);')
            globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')
            globals.ui.txtMobilecli.setStyleSheet('background-color: rgb(255, 255, 220);')
            globals.ui.lblWarning.setText("")
            globals.ui.lblWarning.setStyleSheet('background-color: rgb(255, 255, 200);')

        except Exception as error:
            print("error en cleanCli ", error)

    @staticmethod
    def loadTablecli(varcli):
        try:
            listTabCustomers = Conexion.listCustomers(varcli)
            # print(listTabCustomers)
            index = 0
            for record in listTabCustomers:
                globals.ui.tableCustomerlist.setRowCount(index + 1)
                globals.ui.tableCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tableCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tableCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[5])))
                globals.ui.tableCustomerlist.setItem(index, 3,
                                                     QtWidgets.QTableWidgetItem("   " + str(record[7] + "   ")))
                globals.ui.tableCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.tableCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                if record[10] == "True":
                    globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Alta")))
                else:
                    globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Baja")))
                globals.ui.tableCustomerlist.item(index, 0).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 1).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 4).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 5).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 6).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                index += 1
        except Exception as error:
            print("error en loadTablecli ", error)

    @staticmethod
    def selectCustomer():
        try:
            row = globals.ui.tableCustomerlist.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneCustomer(str(data[2]))
            print(record)
            boxes = [
                globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli,
                globals.ui.txtNamecli, globals.ui.txtEmailcli, globals.ui.txtMobilecli,
                globals.ui.txtDircli
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
    def delCliente():
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Client?")
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

                Customers.loadTablecli(True)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Operation cancelled.")
        except Exception as error:
            print("error delete cliente ", error)

    @staticmethod
    def Historicocli():
        try:
            if globals.ui.chkHistoricocli.isChecked():
                varcli = False
            else:
                varcli = True

            Customers.loadTablecli(varcli)
        except Exception as error:
            print("error en historicocli ", error)

    @staticmethod
    def saveCli(self):
        try:
            newcli = [
                globals.ui.txtDnicli.text(), globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(),
                globals.ui.txtNamecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(), globals.ui.cmbMunicli.currentText()
            ]

            if globals.ui.rbtFacpaper.isChecked():
                fact = "paper"
            elif globals.ui.rbtFacmail.isChecked():
                fact = "electronic"
            else:
                fact = ""

            newcli.append(fact)

            if Conexion.addCli(newcli) and len(newcli) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Cliente added successfully")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("WARNING")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("DNI or mobile exists, or data unfilled.\nContact administrator or try again later.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                mbox.exec()

                Customers.loadTablecli(True)

        except Exception as error:
            print("error en saveCli ", error)


    @staticmethod
    def modifcli():
        try:
            print(globals.estado)
            if globals.estado == str("False"):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Client non activated .Do you want activate?")
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
                modifcli = [
                    globals.ui.txtDnicli.text(), globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(),
                    globals.ui.txtNamecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                    globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(),
                    globals.ui.cmbMunicli.currentText(),globals.estado
                ]

                if globals.ui.rbtFacpaper.isChecked():
                    fact = "paper"
                elif globals.ui.rbtFacmail.isChecked():
                    fact = "electronic"
                    modifcli.append(fact)
                if Conexion.modifcli(dni , modifcli):
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

def buscaCli():
    try :
        record = []
        dni = globals.ui.txtDnicli.text()
        record = Conexion.dataOneCustomer(str(dni))
        print(record)
        if not record :
         mbox = QtWidgets.QMessageBox()
         mbox.setWindowTitle("Information")
         mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
         mbox.setText("Cliente not exists")
         mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        if mbox.exec():
           mbox.hide()
        else :
         box = [globals.ui.txtDnicli , globals.ui.txtAltacli,globals.ui.txtApelcli,globals.ui.txtNamecli,
                       globals.ui.txtEmailcli, globals.ui.txtMobilecli, globals.ui.txtDircli,]
        for i in rage(len(box)):
            box[i].setText(record[i])
        globals.ui.cmbProvcli.setCurrentText(record[7])
        globals.ui.cmbMunicli.setCurrentText(record[8])
        if(str(record[9])) == 'paper':
            globals.ui.rbtFacpapel.setChecked(True)
        else :
            globals.ui.rbtFacmail.setChecked(True)
        if(str(record[10])) == 'False':
            globals.ui.lblWarning.setText("Hystorical Client")
            globals.ui.lblWarning.setStyleSheet("background-color: rgb(255, 255, 200);color : #red")

    except Exception as error:
        print("error busca client", error)
