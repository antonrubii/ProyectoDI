import globals
from PyQt6 import QtCore, QtWidgets, QtGui
from conexion import Conexion


class Products:

    @staticmethod
    def loadTablePro(self=None):
        """
        MÉT0DO: Cargar Tabla de Productos.
        QUÉ HACE: Lee los productos de la BD y los muestra en el QTableWidget. 
        Aplica color ROJO (#FF3B30) a las celdas cuyo stock sea 5 o menos.
        PARA EL EXAMEN: Es la función de "Refrescar". Se llama al iniciar el programa y tras cada cambio (Alta/Baja/Modif).
        """
        try:
            listado = Conexion.listProducts()
            globals.ui.tableProducts.setRowCount(0)  # Limpiar tabla antes de rellenar

            for index, registro in enumerate(listado):
                globals.ui.tableProducts.insertRow(index)
                # Registro BD: [0:Code, 1:Name, 2:Family, 3:Stock, 4:Price]

                # Nombre (Columna 0)
                globals.ui.tableProducts.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[1])))

                # Stock con Lógica de Color (Columna 1)
                stock = int(registro[3])
                item_stock = QtWidgets.QTableWidgetItem(str(stock))
                if stock <= 5:
                    item_stock.setBackground(QtGui.QColor("#FF3B30"))  # Rojo Apple
                    item_stock.setForeground(QtGui.QColor("white"))  # Texto blanco para contraste
                    font = QtGui.QFont()
                    font.setBold(True)
                    item_stock.setFont(font)

                globals.ui.tableProducts.setItem(index, 1, item_stock)

                # Familia y Precio (Columnas 2 y 3)
                globals.ui.tableProducts.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                globals.ui.tableProducts.setItem(index, 3, QtWidgets.QTableWidgetItem(f"{float(registro[4]):.2f} €"))

                # Alineaciones estéticas
                item_stock.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tableProducts.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        except Exception as error:
            print("Error en loadTablePro:", error)

    @staticmethod
    def selectProduct(self=None):
        """
        MÉT0DO: Seleccionar Producto.
        QUÉ HACE: Al hacer clic en la tabla, carga los datos en los LineEdit y guarda el código original en una variable global.
        PARA EL EXAMEN: Guardar el 'old_pro_code' es vital para poder modificar el Código (ID) sin que SQL se pierda.
        """
        try:
            row = globals.ui.tableProducts.selectedItems()
            if not row: return

            # Buscamos el producto por el nombre (que está en la columna 0 de tu tabla)
            nombre_pro = row[0].text()
            registro = Conexion.dataOneProduct(nombre_pro)

            if registro:
                # GUARDAMOS EL CÓDIGO ORIGINAL (Para el WHERE del Update)
                globals.old_pro_code = str(registro[0])

                globals.ui.txtCode.setText(str(registro[0]))
                globals.ui.txtName.setText(str(registro[1]))
                globals.ui.cmbFamily.setCurrentText(str(registro[2]))
                globals.ui.txtStock.setText(str(registro[3]))
                globals.ui.txtPrice.setText(str(registro[4]))

        except Exception as error:
            print("Error en selectProduct:", error)

    @staticmethod
    def savePro(self=None):
        """
        MÉT0DO: Guardar Nuevo Producto.
        QUÉ HACE: Recoge los datos de las cajas y los inserta en la BD.
        PARA EL EXAMEN: Verifica que no haya campos vacíos con 'all()' antes de guardar.
        """
        try:
            nuevo_pro = [
                globals.ui.txtCode.text(),
                globals.ui.txtName.text(),
                globals.ui.cmbFamily.currentText(),
                globals.ui.txtStock.text(),
                globals.ui.txtPrice.text()
            ]

            if all(nuevo_pro):  # Si todos los campos tienen texto
                if Conexion.addPro(nuevo_pro):
                    QtWidgets.QMessageBox.information(None, "Éxito", "Producto guardado")
                    Products.loadTablePro()
                else:
                    QtWidgets.QMessageBox.warning(None, "Error", "El código ya existe")
            else:
                QtWidgets.QMessageBox.warning(None, "Aviso", "Faltan datos por rellenar")

        except Exception as error:
            print("Error en savePro:", error)

    @staticmethod
    def modifPro(self=None):
        """
        MÉT0DO: Modificar Producto.
        QUÉ HACE: Envía los datos nuevos y el código antiguo a la BD para actualizar el registro.
        PARA EL EXAMEN: Usa el 'globals.old_pro_code' que guardamos en selectProduct para localizar el registro en SQL.
        """
        try:
            codigo_nuevo = globals.ui.txtCode.text()
            datos_mod = [
                codigo_nuevo,
                globals.ui.txtName.text(),
                globals.ui.cmbFamily.currentText(),
                globals.ui.txtStock.text(),
                globals.ui.txtPrice.text(),
                globals.old_pro_code  # El código que tenía antes de editar
            ]

            if Conexion.modifPro(datos_mod):
                QtWidgets.QMessageBox.information(None, "Éxito", "Producto actualizado")
                Products.loadTablePro()
            else:
                QtWidgets.QMessageBox.warning(None, "Error", "No se pudo modificar")

        except Exception as error:
            print("Error en modifPro:", error)

    @staticmethod
    def delPro(self=None):
        """
        MÉT0DO: Eliminar Producto.
        QUÉ HACE: Borrado físico (DELETE) del producto tras confirmar con el usuario.
        PARA EL EXAMEN: El borrado de productos suele ser físico (DELETE), a diferencia de clientes que suele ser lógico.
        """
        try:
            codigo = globals.ui.txtCode.text()
            if not codigo: return

            mbox = QtWidgets.QMessageBox.question(None, "Eliminar", f"¿Borrar producto {codigo}?",
                                                  QtWidgets.QMessageBox.StandardButton.Yes |
                                                  QtWidgets.QMessageBox.StandardButton.No)

            if mbox == QtWidgets.QMessageBox.StandardButton.Yes:
                if Conexion.deletePro(codigo):
                    QtWidgets.QMessageBox.information(None, "Éxito", "Eliminado")
                    Products.loadTablePro()
                    # Limpiar campos tras borrar
                    for w in [globals.ui.txtCode, globals.ui.txtName, globals.ui.txtStock, globals.ui.txtPrice]:
                        w.setText("")

        except Exception as error:
            print("Error en delPro:", error)

    @staticmethod
    def checkPrice():
        """
        MÉT0DO: Validar Precio.
        QUÉ HACE: Convierte comas en puntos, asegura que sea un número y lo formatea a 2 decimales.
        PARA EL EXAMEN: Úsalo en el evento 'editingFinished' para que los precios siempre luzcan profesionales (ej: 2.99).
        """
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