import csv
import time
import customers
import conexion
import sys
import zipfile
import shutil
import globals
import time
from PyQt6 import QtWidgets, QtCore, QtGui
from venAux import *
from window import *
import globals
import conexion


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
            list =conexion.Conexion.listProv(self)
            #listado = conexionserver.ConexionServer.listaProv(self)
            globals.ui.cmbProvcli.addItems(list)
        except Exception as e:
            print("error en cargar las provincias", e)

    def loadMunicli(self):
        try:
            province = globals.ui.cmbProvcli.currentText()
            list = conexion.Conexion.listMuniProv(province)
            # listado = conexionserver.ConexionServer.listMuniProv(province)
            globals.ui.cmbMunicli.clear()
            globals.ui.cmbMunicli.addItems(list)
        except Exception as e:
            print("error en cargar los municipios", e)

    def resizeTabCustomer (self):
        try:
            header = globals.ui.tableCustomerlist.horizontalHeader()
            for i in range(header.count()):
                if i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.tableCustomerlist.horizontalHeaderItem(i)
                #negrita en la cabecera
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
            data = datetime.datatime.now().strftime("%Y_/%m_/%d_%H:%M:%S")
            filename = str(data) + '_backup.zip'
            directory , file = globals.dlg.getSaveFileName(None,"Save Backup File",filename, 'zip')
            globals
            if var.dlgOpen.accept and file :

                filezip =zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)
                filezip.write('./data.bbdd.sqlite',os.path.basename('bbdd.sqlite')), zipfile.ZIP_DEFLATED
                filezip.close()
                shutil.move(filezip, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Save Backup')
                mbox.setText('Save Backup Done')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("error in save backup", e)


    def restoreBackup(self):
        try:
            filename = va.dljOpen.getOpenFileName(None,"Restore Backup File", '','*.zip;;All Files (*)')
            file = filename[0]
            if file :
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(path='./data',pwd =None)
                    shutil.move ('bbdd.sqlite' , './data')
                    bbdd.close()
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    mbox.setWindowTitle('Restore Backup')
                    mbox.setText('Restore Backup Done')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    conexion.Conexion.db_conexion(self)
                    events.loadProv(self)
                    cutomers.Customers.loadTableCli(self)
        except Exception as e:
            print("error in restore backup", e)

    def exportXlsCustomers(self):
        try:
            data = datetime.datatime.now().strftime("%Y_/%m_/%d_%H:%M:%S")
            filename = str(data) + '_customers.csv'
            directory, file = globals.dlg.getSaveFileName(None, "Save Backup File", filename, '.csv')
            globals.dlgOpen.centrar()
            var = False

            if file :
                records = conexion.Conexion.listCustomers(var)
                with open (file , 'w',newline='',encoding='utf-8') as csvfile:
                    writer= csv.writer(csvfile)
                    writer.writerows("DNI_NIE","Fecha Alta","Surname","Name","eMail","Mobile","Adress","Province",
                                     "City","InvoiceType","Active",)

                    for record in records:
                        writer.writerow(record)
                shutil.move(file, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Export Customers')
                mbox.setText('Export Customers Done')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            else :
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Export Customers')
                mbox.setText('Export Customers Error')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("error in export customers", e)