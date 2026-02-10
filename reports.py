from reportlab.pdfgen import canvas
import os
import datetime
from conexion import Conexion
import globals


class Reports():

    def __init__(self):
        """
        MÉTDO: Constructor de la clase.
        QUÉ HACE: Crea la carpeta 'reports' si no existe en el proyecto.
        PARA EL EXAMEN: Asegura que el programa no falle al intentar guardar un PDF si la carpeta no está.
        """
        self.rootPath = ".\\reports"
        if not os.path.exists(self.rootPath):
            os.makedirs(self.rootPath)

    def footer(self, titulo):
        """
        MÉTDO: Pie de página común.
        QUÉ HACE: Dibuja una línea, la fecha actual, el título del informe y el número de página.
        PARA EL EXAMEN: Se llama al final de cada página para que todos los informes tengan un aspecto uniforme.
        """
        try:
            globals.report.line(35, 60, 525, 60)  # Línea horizontal inferior
            fecha = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            globals.report.setFont("Helvetica", 7)
            globals.report.drawString(70, 50, fecha)
            globals.report.drawString(250, 50, titulo)
            globals.report.drawString(480, 50, "Página: " + str(globals.report.getPageNumber()))
        except Exception as error:
            print("Error en footer report:", error)

    def topreport(self, titulo):
        """
        MÉTDO: Cabecera común.
        QUÉ HACE: Dibuja el logo, los datos de la empresa (CIF, Dirección) y el título del informe.
        PARA EL EXAMEN: Es donde personalizas la marca de la aplicación. Usa drawImage para el logo y drawCentredString para el título.
        """
        try:
            # Buscamos el logo en varias extensiones por seguridad
            path_logo = './img/logo.png'
            if not os.path.exists(path_logo):
                path_logo = './img/logo.ico'

            globals.report.setFont('Helvetica-Bold', 10)
            globals.report.drawString(55, 785, "EMPRESA TEIS")
            globals.report.drawCentredString(295, 675, titulo)
            globals.report.line(35, 665, 525, 665)  # Línea divisoria cabecera

            if os.path.exists(path_logo):
                globals.report.drawImage(path_logo, 480, 745, width=40, height=40)

            globals.report.setFont('Helvetica', 9)
            globals.report.drawString(55, 755, "CIF : A13425258")
            globals.report.drawString(55, 745, "Avd. de Galicia ,101")
            globals.report.drawString(55, 735, "Vigo - 36215 - España")

            # Dibujamos el recuadro del CIF
            globals.report.rect(50, 695, 110, 105, stroke=1, fill=0)
        except Exception as error:
            print("Error en topreport:", error)

    def reportCustomers(self):
        """
        MÉTDO: Informe General de Clientes.
        QUÉ HACE: Genera un PDF con la lista completa de clientes de la base de datos.
        PARA EL EXAMEN: Muestra cómo iterar sobre una lista de registros y gestionar el salto de página (if y <= 90).
        """
        try:
            fecha_archivo = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre_pdf = fecha_archivo + "_reportcustomers.pdf"
            pdf_path = os.path.join(self.rootPath, nombre_pdf)

            globals.report = canvas.Canvas(pdf_path)
            titulo = "LISTADO CLIENTES"
            self.topreport(titulo)
            self.footer(titulo)

            records = Conexion.listCustomers(False)  # Traer todos los clientes

            # Cabecera de la tabla de datos
            items = ["DNI_NIE", "APELLIDOS", "NOMBRE", "MÓVIL", "CIUDAD", "ESTADO"]
            globals.report.setFont("Helvetica-Bold", 10)
            x_coords = [45, 125, 215, 305, 395, 485]
            for i, text in enumerate(items):
                globals.report.drawString(x_coords[i], 650, text)
            globals.report.line(35, 645, 525, 645)

            y = 630
            for r in records:
                if y <= 90:  # Control de salto de página
                    globals.report.showPage()
                    self.topreport(titulo)
                    self.footer(titulo)
                    y = 630
                globals.report.setFont("Helvetica", 8)
                globals.report.drawString(45, y, str(r[0]))
                globals.report.drawString(125, y, str(r[2]))
                globals.report.drawString(215, y, str(r[3]))
                globals.report.drawString(305, y, str(r[5]))
                globals.report.drawString(395, y, str(r[8]))
                globals.report.drawString(485, y, "Alta" if str(r[10]) == 'True' else "Baja")
                y -= 25

            globals.report.save()
            os.startfile(pdf_path)  # Abre el PDF automáticamente
        except Exception as error:
            print("Error reportCustomers:", error)

    def reportProducts(self):
        """
        MÉTDO: Informe de Almacén.
        QUÉ HACE: Crea una lista de todos los productos, stock y precios.
        PARA EL EXAMEN: Es muy similar al de clientes, pero cambia la tabla y las columnas.
        """
        try:
            fecha_archivo = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre_pdf = fecha_archivo + "_reportproducts.pdf"
            pdf_path = os.path.join(self.rootPath, nombre_pdf)

            globals.report = canvas.Canvas(pdf_path)
            titulo = "LISTADO PRODUCTOS"
            self.topreport(titulo)
            self.footer(titulo)

            records = Conexion.listProducts()

            items = ["ID", "NOMBRE", "FAMILIA", "STOCK", "PRECIO"]
            globals.report.setFont("Helvetica-Bold", 10)
            x_coords = [60, 130, 280, 380, 470]
            for i, text in enumerate(items):
                globals.report.drawString(x_coords[i], 650, text)
            globals.report.line(35, 645, 525, 645)

            y = 630
            for r in records:
                if y <= 90:
                    globals.report.showPage()
                    self.topreport(titulo)
                    self.footer(titulo)
                    y = 630
                globals.report.setFont("Helvetica", 8)
                globals.report.drawString(60, y, str(r[0]))
                globals.report.drawString(130, y, str(r[1]))
                globals.report.drawString(280, y, str(r[2]))
                globals.report.drawCentredString(395, y, str(r[3]))
                globals.report.drawRightString(515, y, f"{r[4]} €")
                y -= 25

            globals.report.save()
            os.startfile(pdf_path)
        except Exception as error:
            print("Error reportProducts:", error)

    def ticket(self):
        """
        MÉTDO: Generar Factura/Ticket.
        QUÉ HACE: Crea un PDF detallado de una factura específica, incluyendo datos del cliente y desglose de productos.
        PARA EL EXAMEN: Este es el métdo más complejo. Calcula el Subtotal, IVA y Total final sumando las líneas de venta.
        """
        try:
            data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            ticket_name = data + "_ticket.pdf"
            pdf_path = os.path.join(self.rootPath, ticket_name)
            globals.report = canvas.Canvas(pdf_path)

            id_fac = globals.ui.lblNumFac.text()
            dni = globals.ui.txtDnifac.text()
            titulo = "FACTURA" if dni != "00000000T" else "FACTURA SIMPLIFICADA"

            self.topreport(titulo)

            # --- Bloque Datos Cliente ---
            records = Conexion.dataOneCustomer(dni)
            if records:
                globals.report.setFont("Helvetica-Bold", 10)
                y_cli = 640
                globals.report.drawString(55, y_cli, "DATOS CLIENTE:")
                globals.report.setFont("Helvetica", 9)
                globals.report.drawString(55, y_cli - 15, f"DNI: {records[0]}")
                globals.report.drawString(55, y_cli - 30, f"CLIENTE: {records[2]}, {records[3]}")
                globals.report.drawString(300, y_cli - 15, f"DIRECCIÓN: {records[6]}")
                globals.report.drawString(300, y_cli - 30, f"LOCALIDAD: {records[8]}")

            # --- Bloque Tabla de Ventas ---
            y_tab = 570
            globals.report.line(35, y_tab, 525, y_tab)
            globals.report.setFont("Helvetica-Bold", 9)
            globals.report.drawString(55, y_tab - 15, "COD.")
            globals.report.drawString(110, y_tab - 15, "PRODUCTO")
            globals.report.drawString(310, y_tab - 15, "CANT.")
            globals.report.drawString(380, y_tab - 15, "PRECIO")
            globals.report.drawString(470, y_tab - 15, "TOTAL")
            globals.report.line(35, y_tab - 20, 525, y_tab - 20)

            # Iterar productos de la factura
            ventas = Conexion.getVentas(id_fac)
            y = y_tab - 35
            suma_subtotal = 0.0

            globals.report.setFont("Helvetica", 9)
            for v in ventas:
                # v = [idv, idpro, nombre, precio, cantidad, total_linea]
                globals.report.drawString(55, y, str(v[1]))
                globals.report.drawString(110, y, str(v[2]))
                globals.report.drawCentredString(325, y, str(v[4]))
                globals.report.drawRightString(420, y, f"{float(v[3]):.2f} €")
                globals.report.drawRightString(515, y, f"{float(v[5]):.2f} €")
                suma_subtotal += float(v[5])  # Acumular para el total
                y -= 20

            # --- Bloque de Totales Finales ---
            y_fin = y - 20
            globals.report.line(350, y_fin + 10, 525, y_fin + 10)
            iva = suma_subtotal * 0.21
            total = suma_subtotal + iva

            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(360, y_fin, "SUBTOTAL:")
            globals.report.drawRightString(515, y_fin, f"{suma_subtotal:.2f} €")
            globals.report.drawString(360, y_fin - 15, "IVA (21%):")
            globals.report.drawRightString(515, y_fin - 15, f"{iva:.2f} €")

            globals.report.setFont("Helvetica-Bold", 11)
            globals.report.setFillColorRGB(0, 0.3, 0.8)  # Azul para resaltar el Total
            globals.report.drawString(360, y_fin - 35, "TOTAL FACTURA:")
            globals.report.drawRightString(515, y_fin - 35, f"{total:.2f} €")

            self.footer(titulo)
            globals.report.save()
            os.startfile(pdf_path)
        except Exception as error:
            print("Error en ticket PDF:", error)