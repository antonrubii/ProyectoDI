from reportlab.pdfgen import canvas
import os
import datetime
from conexion import Conexion
import globals


class Reports():
    def __init__(self):
        self.rootPath = ".\\reports"
        if not os.path.exists(self.rootPath):
            os.makedirs(self.rootPath)

    def footer(self, titulo):
        try:
            globals.report.line(35, 60, 525, 60)
            day = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            globals.report.setFont("Helvetica", 7)
            globals.report.drawString(70, 50, day)
            globals.report.drawString(250, 50, titulo)
            globals.report.drawString(480, 50, "Página: " + str(globals.report.getPageNumber()))
        except Exception as error:
            print("Error en footer report:", error)

    def topreport(self, titulo):
        try:
            path_logo = './img/logo.png'
            if not os.path.exists(path_logo):
                path_logo = './img/logo.ico'

            globals.report.setFont('Helvetica-Bold', 10)
            globals.report.drawString(55, 785, "EMPRESA TEIS")
            globals.report.drawCentredString(295, 675, titulo)
            globals.report.line(35, 665, 525, 665)

            if os.path.exists(path_logo):
                globals.report.drawImage(path_logo, 480, 745, width=40, height=40)

            globals.report.setFont('Helvetica', 9)
            globals.report.drawString(55, 755, "CIF : A13425258")
            globals.report.drawString(55, 745, "Avd. de Galicia ,101")
            globals.report.drawString(55, 735, "Vigo - 36215 - España")
            globals.report.line(50, 800, 160, 800)
            globals.report.line(50, 695, 160, 695)
            globals.report.line(50, 800, 50, 695)
            globals.report.line(160, 800, 160, 695)
        except Exception as error:
            print("Error en topreport:", error)

    def reportCustomers(self):
        try:
            fecha_archivo = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre_pdf = fecha_archivo + "_reportcustomers.pdf"
            pdf_path = os.path.join(self.rootPath, nombre_pdf)

            globals.report = canvas.Canvas(pdf_path)
            titulo = "LISTADO CLIENTES"
            self.topreport(titulo)
            self.footer(titulo)

            # Usamos listCustomers(False) para traer a todos (según tu conexion.py)
            records = Conexion.listCustomers(False)

            items = ["DNI_NIE", "APELLIDOS", "NOMBRE", "MÓVIL", "CIUDAD", "ESTADO"]
            globals.report.setFont("Helvetica-Bold", 10)
            x_coords = [45, 125, 215, 305, 395, 485]
            for i, text in enumerate(items):
                globals.report.drawString(x_coords[i], 650, text)
            globals.report.line(35, 645, 525, 645)

            y = 630
            for r in records:
                if y <= 90:
                    globals.report.showPage()
                    self.topreport(titulo);
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
            os.startfile(pdf_path)
        except Exception as error:
            print("Error reportCustomers:", error)

    def reportProducts(self):
        try:
            fecha_archivo = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            nombre_pdf = fecha_archivo + "_reportproducts.pdf"
            pdf_path = os.path.join(self.rootPath, nombre_pdf)

            globals.report = canvas.Canvas(pdf_path)
            titulo = "LISTADO PRODUCTOS"
            self.topreport(titulo)
            self.footer(titulo)

            # CORRECCIÓN: listProducts no recibe argumentos según tu conexion.py
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
                    self.topreport(titulo);
                    self.footer(titulo)
                    y = 630
                globals.report.setFont("Helvetica", 8)
                # record: [0:Code, 1:Name, 2:Family, 3:Stock, 4:Price]
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
        try:
            # Mantengo tu lógica de ticket actual pero asegurando que abra el archivo
            data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            ticket_name = data + "_ticket.pdf"
            pdf_path = os.path.join(self.rootPath, ticket_name)
            globals.report = canvas.Canvas(pdf_path)

            dni = globals.ui.txtDnifac.text()
            titulo = "FACTURA SIMPLIFICADA" if dni == "00000000T" else "FACTURA"
            records = Conexion.dataOneCustomer(dni)

            self.topreport(titulo)
            if records:
                globals.report.setFont("Helvetica-Bold", 10)
                globals.report.drawString(220, 700, "DNI: " + str(records[0]))
                globals.report.drawString(220, 685, "APELLIDOS: " + str(records[2]))
                globals.report.drawString(220, 670, "NOMBRE: " + str(records[3]))
                globals.report.drawString(220, 655, "DIRECCIÓN: " + str(records[6]))
                globals.report.drawString(220, 640, "LOCALIDAD: " + str(records[8]) + "  PROVINCIA: " + str(records[7]))

            self.footer(titulo)
            globals.report.save()
            os.startfile(pdf_path)
        except Exception as error:
            print("Error en ticket:", error)