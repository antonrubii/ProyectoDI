import csv
import zipfile
import shutil
import os
import sys
import time
import datetime
from PyQt6 import QtWidgets, QtCore, QtGui
import globals
import conexion
import customers


class Events:

    # --- SECCIÓN 1: INTERFAZ Y VENTANAS ---

    @staticmethod
    def messageExit(self=None):
        """
        QUÉ HACE: Abre un cuadro de diálogo para confirmar si el usuario quiere cerrar la app.
        PARA EL EXAMEN: Se conecta a la acción 'Exit' del menú y de la Toolbar.
        Personaliza los botones con 'Si' y 'No' para un toque más profesional.
        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
            mbox.setWindowTitle('Salir')
            mbox.setText('¿Está seguro de que desea salir?')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
        except Exception as e:
            print("Error en salida:", e)

    @staticmethod
    def openCalendar(self=None):
        """QUÉ HACE: Muestra la ventana del calendario. PARA EL EXAMEN: Se conecta al botón del icono de calendario."""
        try:
            globals.vencal.show()
        except Exception as e:
            print("Error abrir calendario:", e)

    @staticmethod
    def loadData(qDate):
        """
        QUÉ HACE: Recibe la fecha clicada en el calendario y la escribe en el campo 'txtAltacli' con formato dd/mm/yyyy.
        PARA EL EXAMEN: Es el mét0do que "captura" la fecha elegida. Se conecta en venAux.py al evento 'clicked' del QCalendarWidget.
        """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            # Solo escribimos si estamos en la pestaña de clientes (índice 0)
            if globals.ui.panPrincipal.currentIndex() == 0:
                globals.ui.txtAltacli.setText(data)
            time.sleep(0.1)
            globals.vencal.hide()
        except Exception as e:
            print("Error cargar fecha:", e)

    # --- SECCIÓN 2: CARGA DE DATOS DINÁMICOS ---

    @staticmethod
    def loadProv(self=None):
        """QUÉ HACE: Llena el ComboBox de provincias desde la BD al arrancar."""
        try:
            globals.ui.cmbProvcli.clear()
            lista = conexion.Conexion.listProv()
            globals.ui.cmbProvcli.addItems(lista)
        except Exception as e:
            print("Error cargar provincias:", e)

    @staticmethod
    def loadMunicli(self=None):
        """
        QUÉ HACE: Llena el ComboBox de municipios filtrando por la provincia seleccionada.
        PARA EL EXAMEN: Se conecta al evento 'currentIndexChanged' del combo de provincias. Es lo que hace que los combos estén vinculados.
        """
        try:
            provincia = globals.ui.cmbProvcli.currentText()
            if provincia:
                lista = conexion.Conexion.listMuniProv(provincia)
                globals.ui.cmbMunicli.clear()
                globals.ui.cmbMunicli.addItems(lista)
        except Exception as e:
            print("Error cargar municipios:", e)

    # --- SECCIÓN 3: CONFIGURACIÓN VISUAL DE TABLAS ---

    @staticmethod
    def resizeTabCustomer(self=None):
        """QUÉ HACE: Ajusta el ancho de las columnas de la tabla de clientes. Pone las cabeceras en negrita."""
        try:
            header = globals.ui.tableCustomerlist.horizontalHeader()
            for i in range(header.count()):
                # La columna 3 (Móvil/DNI según diseño) se ajusta al contenido, el resto se estira.
                if i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception as e:
            print("Error resize clientes:", e)

    @staticmethod
    def resizetableSales(self=None):
        """
        QUÉ HACE: Configura las 6 columnas de la tabla de ventas (Facturación).
        PARA EL EXAMEN: Es fundamental para que la papelera (col 5) se vea siempre sin scroll horizontal.
        """
        try:
            header = globals.ui.tableSales.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # ID
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # Cant
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)  # Producto (se estira)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # Precio
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # Total
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)  # Papelera
            globals.ui.tableSales.setColumnWidth(5, 35)
        except Exception as e:
            print("Error resize ventas:", e)

    @staticmethod
    def resizeTabProducts(self=None):
        """QUÉ HACE: Ajusta las columnas de la tabla de productos (Almacén)."""
        try:
            header = globals.ui.tableProducts.horizontalHeader()
            for i in range(header.count()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception as e:
            print("Error resize productos:", e)

    # --- SECCIÓN 4: HERRAMIENTAS (BACKUP Y EXPORTACIÓN) ---

    @staticmethod
    def saveBackup(self=None):
        """
        QUÉ HACE: Crea un archivo comprimido .zip de la base de datos actual.
        PARA EL EXAMEN: Usa 'zipfile'. Pregunta al usuario dónde quiere guardar el archivo.
        """
        try:
            fecha = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre = f"{fecha}_backup.zip"
            # Abrir selector de archivos para guardar
            file, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar Copia", nombre, 'Zip (*.zip)')

            if file:
                with zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED) as Fzip:
                    Fzip.write('./data/bbdd.sqlite', 'bbdd.sqlite')
                QtWidgets.QMessageBox.information(None, "Ok", "Copia guardada")
        except Exception as e:
            print("Error Backup:", e)

    @staticmethod
    def restoreBackup(self=None):
        """
        QUÉ HACE: Sustituye la base de datos actual por una que el usuario elija de un archivo .zip.
        PARA EL EXAMEN: Después de extraer, hay que reconectar la BD y recargar las tablas para ver los datos.
        """
        try:
            file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Restaurar Copia", '', 'Zip (*.zip)')
            if file:
                with zipfile.ZipFile(file, 'r') as Fzip:
                    Fzip.extractall('./data')
                QtWidgets.QMessageBox.information(None, "Ok", "Copia restaurada")
                # Reconectar y recargar t0do
                conexion.Conexion.db_connect("./data/bbdd.sqlite")
                Events.loadProv()
                customers.Customers.loadTablecli(True)
        except Exception as e:
            print("Error Restaurar:", e)

    @staticmethod
    def exportXlsCustomers(self=None):
        """
        QUÉ HACE: Genera un archivo .csv con todos los datos de los clientes.
        PARA EL EXAMEN: Usa el módulo 'csv' de Python. Ideal para que el profesor vea exportación de datos.
        """
        try:
            fecha = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre = f"{fecha}_clientes.csv"
            file, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Exportar CSV", nombre, 'CSV (*.csv)')

            if file:
                registros = conexion.Conexion.listCustomers(False)  # Traer todos
                with open(file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        ["DNI", "ALTA", "APELLIDO", "NOMBRE", "MAIL", "MOVIL", "DIR", "PROV", "MUNI", "PAGO", "HIST"])
                    writer.writerows(registros)
                QtWidgets.QMessageBox.information(None, "Ok", "Datos exportados")
        except Exception as e:
            print("Error Exportar:", e)

    # --- SECCIÓN 5: OTROS ---

    @staticmethod
    def loadStatubar(self=None):
        """QUÉ HACE: Inicializa la barra inferior con la fecha y un mensaje de estado."""
        try:
            fecha = datetime.datetime.now().strftime("%d/%m/%Y")
            globals.ui.statusbar.showMessage(f"Bienvenido a EmpresaTeis | Fecha: {fecha} | Estado: Listo")
        except Exception as e:
            print("Error statusbar:", e)

    @staticmethod
    def messageAbout(self=None):
        """QUÉ HACE: Muestra la ventana 'Acerca de'."""
        globals.about.show()

    @staticmethod
    def closeAbout(self=None):
        """QUÉ HACE: Cierra la ventana 'Acerca de'."""
        globals.about.hide()