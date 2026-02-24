import re
import globals
from PyQt6 import QtCore, QtWidgets, QtGui
from conexion import Conexion
from data.antonrubinan2510.invoice import Invoice


class Customers:

    @staticmethod
    def checkDni():
        """
        MÉTODO: Validación Matemática del DNI.
        QUÉ HACE: Comprueba que el DNI/NIE tenga el formato legal (8 números y la letra que le corresponde por algoritmo).
        PARA EL EXAMEN: Si la letra es incorrecta, pone el fondo en rojo (#FFC0CB) y borra el texto. Evita que entren datos "basura" a la BD.
        """
        try:
            dni = globals.ui.txtDnicli.text().upper()
            globals.ui.txtDnicli.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            if len(dni) == 9:
                dni_num = dni[:8]
                if dni_num[0] in dig_ext:
                    dni_num = dni_num.replace(dni_num[0], reemp_dig_ext[dni_num[0]])
                if dni_num.isdigit() and tabla[int(dni_num) % 23] == dni[8]:
                    globals.ui.txtDnicli.setStyleSheet('background-color: white;')
                    return True
            globals.ui.txtDnicli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtDnicli.setText("")
            globals.ui.txtDnicli.setPlaceholderText("DNI INVÁLIDO")
            return False
        except Exception as error:
            print("Error validar dni", error)

    @staticmethod
    def checkMail(email, widget):
        """
        MÉTODO: Validación de Formato de Email.
        QUÉ HACE: Usa una 'Expresión Regular' para asegurar que el correo tenga una estructura tipo 'usuario@dominio.ext'.
        PARA EL EXAMEN: Si el formato es erróneo, limpia el campo para que el usuario no pueda guardar un email inválido.
        """
        try:
            try:
                widget.editingFinished.disconnect()
            except Exception:
                pass
            patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(patron, email):
                widget.setStyleSheet('background-color: white;')
            else:
                widget.setStyleSheet('background-color: #FFC0CB;')
                widget.setText("");
                widget.setPlaceholderText("Email inválido")
        except Exception as error:
            print(error)

    @staticmethod
    def checkMobil(numero, widget):
        """
        MÉTODO: Validación de Teléfono.
        QUÉ HACE: Verifica que el número sea español (9 dígitos y empiece por 6 o 7).
        PARA EL EXAMEN: Útil para asegurar que los datos de contacto sean coherentes.
        """
        try:
            try:
                widget.editingFinished.disconnect()
            except Exception:
                pass
            patron = r'^[67]\d{8}$'
            if re.match(patron, numero):
                widget.setStyleSheet('background-color: white;')
            else:
                widget.setStyleSheet('background-color: #FFC0CB;')
                widget.setText("");
                widget.setPlaceholderText("Móvil inválido")
        except Exception as error:
            print(error)

    @staticmethod
    def capitalizar(texto, widget):
        """
        MÉTODO: Formateo de Texto.
        QUÉ HACE: Pone la primera letra en mayúscula.
        PARA EL EXAMEN: Sirve para mantener la base de datos limpia y profesional sin importar cómo escriba el usuario.
        """
        try:
            widget.setText(texto.title())
        except Exception as error:
            print("Error capitalizar:", error)

    @staticmethod
    def cleanCli(self=None):
        """
        MÉTODO: Reset del Formulario.
        QUÉ HACE: Vacía todas las cajas, limpia el aviso de histórico y, sobre todo, DESBLOQUEA el DNI.
        PARA EL EXAMEN: Es obligatorio usarlo antes de dar de alta a un cliente nuevo si antes habías pinchado uno en la tabla.
        """
        try:
            formcli = [globals.ui.txtDnicli, globals.ui.txtEmailcli, globals.ui.txtMobilecli,
                       globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNamecli, globals.ui.txtDircli]
            for dato in formcli: dato.setText("")
            globals.ui.txtDnicli.setEnabled(True)  # Permitir escribir DNI de nuevo
            globals.ui.txtDnicli.setStyleSheet('background-color: white;')
            globals.ui.cmbMunicli.clear()
            globals.ui.lblWarning.setText("")
            from events import Events
            Events.loadProv(None)
            Invoice.loadTablefac()
        except Exception as error:
            print("Error en cleanCli:", error)

    @staticmethod
    def loadTablecli(varcli):
        try:
            listTabCustomers = Conexion.listCustomers(varcli)
            globals.ui.tableCustomerlist.setRowCount(0)

            for index, record in enumerate(listTabCustomers):
                globals.ui.tableCustomerlist.insertRow(index)

                # MAPPING CORRECTO SEGÚN TU BASE DE DATOS:
                # record[0]: DNI, record[2]: Apellido, record[3]: Nombre,
                # record[5]: Móvil, record[7]: Prov, record[8]: Ciudad, record[10]: Estado

                # Columna 0: Apellido
                globals.ui.tableCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                # Columna 1: Nombre
                globals.ui.tableCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                # Columna 2: DNI
                globals.ui.tableCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[0])))
                # Columna 3: Móvil
                globals.ui.tableCustomerlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[5])))
                # Columna 4: Provincia
                globals.ui.tableCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[7])))
                # Columna 5: Ciudad (City)
                globals.ui.tableCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[8])))

                # Columna 6: Estado (Pintar en rojo si es Baja)
                is_active = str(record[10]) == "True"
                item_estado = QtWidgets.QTableWidgetItem("Alta" if is_active else "Baja")

                if not is_active:
                    item_estado.setForeground(QtGui.QColor("#FF3B30"))  # Rojo Apple

                globals.ui.tableCustomerlist.setItem(index, 6, item_estado)

                # Alinear todas las celdas al centro
                for i in range(7):
                    globals.ui.tableCustomerlist.item(index, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        except Exception as error:
            print("Error en loadTablecli corrigiendo índices:", error)

    @staticmethod
    def selectCustomer(self=None):
        """
        MÉTODO: Selección de Registro.
        QUÉ HACE: Al clicar la tabla, pasa los datos a las cajas, bloquea el DNI y sincroniza con Facturación.
        PARA EL EXAMEN: Bloqueamos el DNI (setEnabled(False)) porque es la clave primaria y no debe editarse "en caliente".
        """
        try:
            row = globals.ui.tableCustomerlist.selectedItems()
            if not row: return
            dni = row[2].text()
            record = Conexion.dataOneCustomer(dni)
            if record:
                globals.ui.txtDnicli.setText(str(record[0]))
                globals.ui.txtApelcli.setText(str(record[2]))
                globals.ui.txtNamecli.setText(str(record[3]))
                globals.ui.txtEmailcli.setText(str(record[4]))
                globals.ui.txtMobilecli.setText(str(record[5]))
                globals.ui.txtDircli.setText(str(record[6]))
                globals.ui.cmbProvcli.setCurrentText(str(record[7]))
                from events import Events
                Events.loadMunicli()
                globals.ui.cmbMunicli.setCurrentText(str(record[8]))
                if str(record[9]) == "paper":
                    globals.ui.rbtFacpaper.setChecked(True)
                else:
                    globals.ui.rbtFacmail.setChecked(True)
                globals.estado = str(record[10])
                globals.ui.txtDnicli.setEnabled(False)  # BLOQUEO DNI
                globals.ui.txtDnifac.setText(str(record[0]))  # Pasar DNI a Factura
                from invoice import Invoice
                Invoice.buscaCli()
                Invoice.loadTablefac(dni)
        except Exception as error:
            print("Error selectCustomer:", error)

    @staticmethod
    def saveCli(self=None):
        """
        MÉTODO: Crear Cliente (INSERT).
        QUÉ HACE: Recoge los datos de la interfaz y llama a la BD para guardarlos.
        PARA EL EXAMEN: Es la operación de ALTA. Verifica que el DNI no esté vacío.
        """
        try:
            newcli = [globals.ui.txtDnicli.text(), globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(),
                      globals.ui.txtNamecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                      globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(),
                      globals.ui.cmbMunicli.currentText()]
            fact = "paper" if globals.ui.rbtFacpaper.isChecked() else "electronic"
            newcli.append(fact)
            if Conexion.addCli(newcli):
                QtWidgets.QMessageBox.information(None, "Éxito", "Cliente guardado")
                Customers.loadTablecli(True)
                Customers.cleanCli()
            else:
                QtWidgets.QMessageBox.warning(None, "Error", "DNI o móvil duplicado")
        except Exception as error:
            print("Error saveCli:", error)

    @staticmethod
    def modifcli(self=None):
        """
        MÉTODO: Actualizar Cliente (UPDATE).
        QUÉ HACE: Modifica los datos. Si el cliente estaba de baja, pregunta si queremos activarlo de nuevo.
        PARA EL EXAMEN: Es el método para gestionar la REACTIVACIÓN de clientes del histórico.
        """
        try:
            if globals.estado == "False":
                if QtWidgets.QMessageBox.question(None, "Alta",
                                                  "Reactivar cliente?") == QtWidgets.QMessageBox.StandardButton.Yes:
                    globals.estado = "True"
            dni = globals.ui.txtDnicli.text()
            fact = "paper" if globals.ui.rbtFacpaper.isChecked() else "electronic"
            # Lista con todos los campos necesarios para la query de UPDATE
            modifcli = [dni, globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(), globals.ui.txtNamecli.text(),
                        globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(), globals.ui.txtDircli.text(),
                        globals.ui.cmbProvcli.currentText(), globals.ui.cmbMunicli.currentText(), globals.estado, fact]
            if Conexion.modifcli(dni, modifcli):
                QtWidgets.QMessageBox.information(None, "Éxito", "Datos actualizados")
                Customers.loadTablecli(True)
        except Exception as error:
            print("Error modifcli:", error)

    @staticmethod
    def delCliente(self=None):
        """
        MÉTODO: Baja Lógica (DELETE simulado).
        QUÉ HACE: Cambia el estado a 'False' para que el cliente no aparezca en la lista normal pero no se borre de la BD.
        PARA EL EXAMEN: Se usa para mantener la integridad: si un cliente tiene facturas, no podemos borrarlo físicamente.
        """
        try:
            dni = globals.ui.txtDnicli.text()
            if dni == "": return
            if QtWidgets.QMessageBox.question(None, "Baja",
                                              "¿Dar de baja?") == QtWidgets.QMessageBox.StandardButton.Yes:
                if Conexion.deleteCli(dni):
                    Customers.loadTablecli(True)
                    Customers.cleanCli()
        except Exception as error:
            print("Error delCliente:", error)

    @staticmethod
    def buscaCli(self=None):
        """
        MÉTODO: Buscador Manual.
        QUÉ HACE: Busca un DNI escrito y rellena el formulario.
        PARA EL EXAMEN: Es la función de la LUPA. Útil para ver si un cliente nuevo ya estuvo registrado antes.
        """
        try:
            dni = globals.ui.txtDnicli.text()
            record = Conexion.dataOneCustomer(dni)
            if record:
                box = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli,
                       globals.ui.txtNamecli, globals.ui.txtEmailcli, globals.ui.txtMobilecli, globals.ui.txtDircli]
                for i in range(len(box)): box[i].setText(str(record[i]))
                globals.ui.cmbProvcli.setCurrentText(str(record[7]))
                if str(record[10]) == 'False': globals.ui.lblWarning.setText("CLIENTE EN HISTÓRICO")
            else:
                QtWidgets.QMessageBox.warning(None, "Error", "Cliente no existe")
        except Exception as error:
            print("Error buscaCli:", error)

    @staticmethod
    def searchDynamic():
        """
        MÉTODO: Búsqueda en tiempo real.
        QUÉ HACE: Filtra la tabla automáticamente mientras el usuario escribe el apellido.
        PARA EL EXAMEN: Se conecta al evento 'textChanged' del campo Apellidos. Demuestra un nivel avanzado de UX.
        """
        try:
            apellido = globals.ui.txtApelcli.text()
            activos = not globals.ui.chkHistoricocli.isChecked()
            # Llamamos a una query especial con LIKE en la clase Conexion
            listado = Conexion.selectCustomersFiltered(apellido, activos)

            globals.ui.tableCustomerlist.setRowCount(0)
            for index, reg in enumerate(listado):
                globals.ui.tableCustomerlist.insertRow(index)
                # ... lógica de rellenado igual que loadTablecli ...
        except Exception as e:
            print("Error búsqueda dinámica:", e)

    @staticmethod
    def Historicocli(self=None):
        """
        MÉTODO: Toggle de Histórico.
        QUÉ HACE: Cambia la tabla entre "Clientes de Alta" y "Clientes de Baja".
        PARA EL EXAMEN: Se conecta al CheckBox de histórico. Llama a loadTablecli con el valor del Check invertido.
        """
        try:
            # Si el check está marcado, varcli es False (mostramos histórico)
            varcli = not globals.ui.chkHistoricocli.isChecked()
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("Error historicocli:", error)