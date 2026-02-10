import re
import globals
from PyQt6 import QtCore, QtWidgets, QtGui
from conexion import Conexion

class Customers:

    # --- SECCIÓN 1: VALIDACIONES Y FORMATO ---

    @staticmethod
    def checkDni():
        """
        QUÉ HACE: Valida el algoritmo del DNI (8 números + letra).
        PARA EL EXAMEN: Si la letra no coincide, borra el campo y avisa en rojo.
        Se usa para evitar datos falsos en la base de datos.
        """
        try:
            dni = globals.ui.txtDnicli.text().upper()
            globals.ui.txtDnicli.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            if len(dni) == 9:
                dig_control = dni[8]
                dni_num = dni[:8]
                if dni_num[0] in dig_ext:
                    dni_num = dni_num.replace(dni_num[0], reemp_dig_ext[dni_num[0]])
                if dni_num.isdigit() and tabla[int(dni_num) % 23] == dig_control:
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
        QUÉ HACE: Usa una 'Expresión Regular' para ver si el correo tiene '@' y '.com/es...'.
        PARA EL EXAMEN: Útil para validar que el campo Email no sea cualquier texto.
        """
        try:
            try: widget.editingFinished.disconnect()
            except Exception: pass
            patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(patron, email):
                widget.setStyleSheet('background-color: white;')
            else:
                widget.setStyleSheet('background-color: #FFC0CB;')
                widget.setText(""); widget.setPlaceholderText("Invalid email")
        except Exception as error:
            print(error)

    @staticmethod
    def checkMobil(numero, widget):
        """
        QUÉ HACE: Valida que el móvil empiece por 6 o 7 y tenga 9 dígitos.
        PARA EL EXAMEN: Evita que metan letras o números de teléfono mal formateados.
        """
        try:
            try: widget.editingFinished.disconnect()
            except Exception: pass
            patron = r'^[67]\d{8}$'
            if re.match(patron, numero):
                widget.setStyleSheet('background-color: white;')
            else:
                widget.setStyleSheet('background-color: #FFC0CB;')
                widget.setText(""); widget.setPlaceholderText("Invalid mobile")
        except Exception as error:
            print(error)

    @staticmethod
    def capitalizar(texto, widget):
        """
        QUÉ HACE: Pone la primera letra en mayúscula (Juan Perez).
        PARA EL EXAMEN: Sirve para que la base de datos quede bonita y ordenada automáticamente.
        """
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("Error en capitalizar ", error)

    # --- SECCIÓN 2: VISUALIZACIÓN (TABLAS Y SELECCIÓN) ---

    @staticmethod
    def loadTablecli(varcli):
        """
        QUÉ HACE: Borra la tabla visual y la rellena con lo que diga la Base de Datos.
        PARA EL EXAMEN: Es el mét0do que 'refresca' la vista. Se llama siempre después de Guardar, Modificar o Borrar.
        """
        try:
            listTabCustomers = Conexion.listCustomers(varcli)
            index = 0
            globals.ui.tableCustomerlist.setRowCount(0) # Limpieza inicial
            for record in listTabCustomers:
                globals.ui.tableCustomerlist.setRowCount(index + 1)
                globals.ui.tableCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tableCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tableCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[0]))) # DNI
                globals.ui.tableCustomerlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[7])))
                globals.ui.tableCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.tableCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                estado = "Alta" if record[10] == "True" else "Baja"
                globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(estado))
                index += 1
        except Exception as error:
            print("error en loadTablecli ", error)

    @staticmethod
    def selectCustomer(self=None):
        """
        QUÉ HACE: Captura el DNI de la fila clicada y rellena los campos de texto.
        PARA EL EXAMEN: Bloquea el campo DNI (setEnabled(False)) para que no se pueda cambiar la clave primaria.
        """
        try:
            row = globals.ui.tableCustomerlist.selectedItems()
            if not row: return
            dni = row[2].text()
            record = Conexion.dataOneCustomer(dni)
            if record:
                # Rellena cajas
                globals.ui.txtDnicli.setText(str(record[0]))
                globals.ui.txtAltacli.setText(str(record[1]))
                globals.ui.txtApelcli.setText(str(record[2]))
                globals.ui.txtNamecli.setText(str(record[3]))
                globals.ui.txtEmailcli.setText(str(record[4]))
                globals.ui.txtMobilecli.setText(str(record[5]))
                globals.ui.txtDircli.setText(str(record[6]))
                # Combos
                globals.ui.cmbProvcli.setCurrentText(str(record[7]))
                from events import Events
                Events.loadMunicli()
                globals.ui.cmbMunicli.setCurrentText(str(record[8]))
                # Radios
                if str(record[9]) == "paper": globals.ui.rbtFacpaper.setChecked(True)
                else: globals.ui.rbtFacmail.setChecked(True)
                # Lógica Facturación
                globals.estado = str(record[10])
                globals.ui.txtDnicli.setEnabled(False) # Bloqueo DNI
                globals.ui.txtDnifac.setText(str(record[0]))
                from invoice import Invoice
                Invoice.buscaCli()
        except Exception as error:
            print("error en selectCustomer", error)

    # --- SECCIÓN 3: OPERACIONES (CRUD) ---

    @staticmethod
    def saveCli(self=None):
        """
        QUÉ HACE: Recoge t0do lo que hay en las cajas y lo manda a la BD.
        PARA EL EXAMEN: Es el botón 'Guardar'. Recuerda usar loadTablecli(True) al final para ver el cambio.
        """
        try:
            newcli = [
                globals.ui.txtDnicli.text(), globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(),
                globals.ui.txtNamecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(), globals.ui.cmbMunicli.currentText()
            ]
            fact = "paper" if globals.ui.rbtFacpaper.isChecked() else "electronic"
            newcli.append(fact)
            if Conexion.addCli(newcli):
                QtWidgets.QMessageBox.information(None, "Ok", "Cliente añadido")
                Customers.loadTablecli(True)
                Customers.cleanCli()
            else:
                QtWidgets.QMessageBox.warning(None, "Error", "DNI o móvil ya existen")
        except Exception as error:
            print("error en saveCli ", error)

    @staticmethod
    def modifcli(self=None):
        """
        QUÉ HACE: Actualiza un cliente. Si estaba de baja, te pregunta si quieres darle de alta.
        PARA EL EXAMEN: El mét0do más completo. Recoge datos + reactivación lógica.
        """
        try:
            if globals.estado == "False":
                if QtWidgets.QMessageBox.question(None, "Alta", "Reactivar?") == QtWidgets.QMessageBox.StandardButton.Yes:
                    globals.estado = "True"
            dni = globals.ui.txtDnicli.text()
            fact = "paper" if globals.ui.rbtFacpaper.isChecked() else "electronic"
            modifcli = [
                dni, globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(),
                globals.ui.txtNamecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(),
                globals.ui.cmbMunicli.currentText(), globals.estado, fact
            ]
            if Conexion.modifcli(dni, modifcli):
                QtWidgets.QMessageBox.information(None, "OK", "Modificado")
                Customers.loadTablecli(True)
        except Exception as error:
            print("error modify client", error)

    @staticmethod
    def delCliente(self=None):
        """
        QUÉ HACE: Baja lógica (Historical = False). No borra el registro físicamente.
        PARA EL EXAMEN: El botón 'Borrar'. Pregunta siempre antes de hacerlo.
        """
        try:
            if QtWidgets.QMessageBox.question(None, "Baja", "Confirmar baja?") == QtWidgets.QMessageBox.StandardButton.Yes:
                dni = globals.ui.txtDnicli.text()
                if Conexion.deleteCli(dni):
                    Customers.loadTablecli(True)
                    Customers.cleanCli()
        except Exception as error:
            print("error delete cliente ", error)

    # --- SECCIÓN 4: UTILIDADES ---

    @staticmethod
    def buscaCli(self=None):
        """
        MÉT0DO: Buscar Cliente por DNI.
        QUÉ HACE:
            1. Valida el formato del DNI (letra correcta).
            2. Si es válido, busca en la BD.
            3. Si existe, llena los campos y bloquea el DNI para edición.
            4. Si no existe o el formato es malo, avisa al usuario.
        PARA EL EXAMEN: Se conecta al botón de la Lupa (btnBuscacli).
        """
        try:
            dni = globals.ui.txtDnicli.text().upper().strip()

            # 1. Validar que el campo no esté vacío
            if dni == "":
                QtWidgets.QMessageBox.warning(None, "Aviso", "Por favor, introduce un DNI para buscar.")
                return

            # 2. Validar formato/letra (aprovechamos el mét0do que ya tienes)
            if not Customers.checkDni():
                # El mét0do checkDni ya pone el color rojo y limpia el campo si falla
                QtWidgets.QMessageBox.warning(None, "DNI Inválido", "El formato del DNI no es correcto.")
                return

            # 3. Buscar en la Base de Datos
            record = Conexion.dataOneCustomer(dni)

            if record:
                # Si record tiene datos, los cargamos en la interfaz
                # record: [0:dni, 1:alta, 2:apel, 3:nome, 4:mail, 5:movil, 6:dir, 7:prov, 8:muni, 9:pago, 10:hist]
                globals.ui.txtAltacli.setText(str(record[1]))
                globals.ui.txtApelcli.setText(str(record[2]))
                globals.ui.txtNamecli.setText(str(record[3]))
                globals.ui.txtEmailcli.setText(str(record[4]))
                globals.ui.txtMobilecli.setText(str(record[5]))
                globals.ui.txtDircli.setText(str(record[6]))

                # Cargar Provincias y Municipios (Bloqueamos señales para evitar errores)
                globals.ui.cmbProvcli.blockSignals(True)
                globals.ui.cmbProvcli.setCurrentText(str(record[7]))
                from events import Events
                Events.loadMunicli()  # Carga los pueblos de esa provincia
                globals.ui.cmbMunicli.setCurrentText(str(record[8]))
                globals.ui.cmbProvcli.blockSignals(False)

                # Cargar el RadioButton del tipo de factura
                if str(record[9]) == "paper":
                    globals.ui.rbtFacpaper.setChecked(True)
                else:
                    globals.ui.rbtFacmail.setChecked(True)

                # Guardar el estado (Alta/Baja) y bloquear el DNI
                globals.estado = str(record[10])
                globals.ui.txtDnicli.setEnabled(False)

                # Opcional: Avisar si es un cliente que estaba dado de baja
                if globals.estado == "False":
                    globals.ui.lblWarning.setText("CLIENTE EN HISTÓRICO")
                    globals.ui.lblWarning.setStyleSheet("color: red; font-weight: bold;")
                else:
                    globals.ui.lblWarning.setText("Cliente encontrado")
                    globals.ui.lblWarning.setStyleSheet("color: green; font-weight: bold;")

            else:
                # 4. Si no existe en la Base de Datos
                QtWidgets.QMessageBox.information(None, "Sin resultados", f"No existe ningún cliente con el DNI: {dni}")
                Customers.cleanCli()  # Limpiamos el formulario para que no queden datos viejos

        except Exception as error:
            print("Error en buscaCli logic:", error)
    @staticmethod
    def Historicocli(self=None):
        """
        QUÉ HACE: Alterna la tabla entre clientes de Alta y clientes de Baja.
        PARA EL EXAMEN: Conéctalo al 'stateChanged' del CheckBox de Histórico.
        """
        try:
            varcli = not globals.ui.chkHistoricocli.isChecked() # True=Activos, False=Bajas
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("error en historicocli ", error)

    @staticmethod
    def cleanCli(self=None):
        """
        QUÉ HACE: Resetea t0do el formulario a blanco y DESBLOQUEA el DNI.
        PARA EL EXAMEN: Se usa en el botón 'Limpiar' para poder añadir clientes nuevos.
        """
        try:
            widgets = [globals.ui.txtDnicli, globals.ui.txtEmailcli, globals.ui.txtMobilecli,
                       globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNamecli, globals.ui.txtDircli]
            for d in widgets: d.setText("")
            globals.ui.txtDnicli.setEnabled(True) # ¡Vuelve a dejar escribir!
            globals.ui.txtDnicli.setStyleSheet('background-color: white;')
            globals.ui.lblWarning.setText(""); globals.ui.cmbMunicli.clear()
            from events import Events
            Events.loadProv(None)
        except Exception as error:
            print("error en cleanCli ", error)