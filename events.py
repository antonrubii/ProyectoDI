import csv
import time
import customers
import conexion
import sys
import zipfile
import shutil
import globals
from PyQt6 import QtWidgets, QtCore, QtGui
from venAux import *
from window import *
import datetime
import os


class Events:
    @staticmethod
    def messageExit(self=None):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon('./img/logo.jpg'))
            mbox.setWindowTitle('Exit')
            mbox.setText('Are you sure you want to exit?')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
            mbox.resize(600, 800)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
            else:
                mbox.hide()
        except Exception as e:
            print("Error en salida", e)

    def openCalendar(self):
        try:
            globals.vencal.show()
        except Exception as e:
            print("Error en calendario", e)

    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.panPrincipal.currentIndex() == 0:
                globals.ui.txtAltacli.setText(data)
            time.sleep(0.3)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)

    def loadProv(self):
        try:
            globals.ui.cmbProvcli.clear()
            lista = conexion.Conexion.listProv()
            globals.ui.cmbProvcli.addItems(lista)
        except Exception as e:
            print("error en cargar las provincias", e)

    def loadMunicli(self=None):
        try:
            province = globals.ui.cmbProvcli.currentText()
            if province:  # Solo si hay algo seleccionado
                lista = conexion.Conexion.listMuniProv(province)
                globals.ui.cmbMunicli.clear()
                globals.ui.cmbMunicli.addItems(lista)
        except Exception as e:
            print("error en cargar los municipios", e)

    def resizeTabCustomer(self):
        try:
            header = globals.ui.tableCustomerlist.horizontalHeader()
            for i in range(header.count()):
                if i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

                header_items = globals.ui.tableCustomerlist.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize la tabla", e)

    def resizetableSales(self):
        try:
            header = globals.ui.tableSales.horizontalHeader()
            for i in range(header.count()):
                if i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

                header_items = globals.ui.tableSales.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

            globals.ui.tableSales.setRowCount(1)
        except Exception as e:
            print("error en resize la tabla", e)

    def resizeTabProducts(self):
        try:
            header = globals.ui.tableProducts.horizontalHeader()
            for i in range(header.count()):


                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

                header_items = globals.ui.tableProducts.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize la tabla", e)

    def messageAbout(self):
        try:
            globals.about.show()
        except Exception as e:
            print("error en abrir about", e)

    def closeAbout(self):
        try:
            globals.about.hide()
        except Exception as e:
            print("error in close about", e)

    def saveBackup(self):
        try:
            data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = str(data) + '_backup.zip'

            # Usamos QtWidgets directamente para no depender de globals.dlg
            file, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar Copia de Seguridad", filename,
                                                            'Zip Files (*.zip)')

            if file:
                filezip = zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)
                # Asegúrate de que esta ruta a tu bbdd sea correcta
                filezip.write('./data/bbdd.sqlite', 'bbdd.sqlite')
                filezip.close()

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Copia de Seguridad')
                mbox.setText('Copia de seguridad realizada con éxito')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("error in save backup", e)

    def restoreBackup(self):
        try:
            # Usamos QtWidgets directamente para evitar el error de atributo
            file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Restaurar Copia de Seguridad", '',
                                                            'Zip Files (*.zip)')

            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(path='./data')

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Restaurar Copia')
                mbox.setText('Copia de seguridad restaurada con éxito')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

                # Recargamos todo para que se vean los cambios
                conexion.Conexion.db_connect("./data/bbdd.sqlite")
                self.loadProv()
                customers.Customers.loadTablecli(True)
        except Exception as e:
            print("error in restore backup", e)

    def exportXlsCustomers(self):
        try:
            data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = str(data) + '_customers.csv'
            directory, file = globals.dlg.getSaveFileName(None, "Save Customers File", filename, '.csv')

            if file:
                records = conexion.Conexion.listCustomers(False)

                with open(file, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        ["DNI_NIE", "Fecha Alta", "Surname", "Name", "eMail", "Mobile",
                         "Adress", "Province", "City", "InvoiceType", "Active"]
                    )

                    for record in records:
                        writer.writerow(record)

                shutil.move(file, directory)

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Export Customers')
                mbox.setText('Export Customers Error')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()


        except Exception as e:
            print("error in export customers", e)

    def loadStatubar(self):
        try:
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            self.labelstatus = QtWidgets.QLabel(self)
            self.labelstatus.setText("Status")
            self.labelstatus.setStyleSheet("color : white; font-weight: bold;font-size: 10px;")
            globals.ui.statusbar.addPermanentWidget(self.labelstatus,1)

        except Exception as e:
            print("error in status bar", e)