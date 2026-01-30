from reportlab.pdfgen import canvas
import os
import datetime
from PIL import Image
from conexion import *
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
            print(error)

    def topreport(self, titulo):
        try:
            path_logo = '.\\img\\logo.ico'
            logo = Image.open(path_logo)
            if isinstance(logo, Image.Image):
                globals.report.setFont('Helvetica-Bold', 10)
                globals.report.drawString(55, 785, "EMPRESA TEIS")
                globals.report.drawCentredString(295, 675, titulo)
                globals.report.line(35, 665, 525, 665)
                globals.report.drawImage(path_logo, 490, 745, width=40, height=40)

                globals.report.setFont('Helvetica', 9)
                globals.report.drawString(55, 755, "CIF : A13425258")
                globals.report.drawString(55, 745, "Avd. de Galicia ,101")
                globals.report.drawString(55, 735, "Vigo -36215 -España")
                globals.report.drawString(55, 725, "Tlfo :986 123 456")
                globals.report.drawString(55, 715, "email :teis@mail.com")

                globals.report.line(50, 800, 160, 800)
                globals.report.line(50, 695, 160, 695)
                globals.report.line(50, 800, 50, 695)
                globals.report.line(160, 800, 160, 695)
        except Exception as error:
            print("Error en topreport:", error)

    def reportCustomers(self):
        try:
            data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            namereporcli = data + "_reportcustomers.pdf"
            pdf_path = os.path.join(self.rootPath, namereporcli)
            globals.report = canvas.Canvas(pdf_path)

            titulo = "lISTADO CLIENTES"
            self.footer(titulo)
            self.topreport(titulo)

            records = Conexion.listCustomers(False)
            if not records:
                print("no customers found")
                return

            items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(45, 650, items[0])
            globals.report.drawString(105, 650, items[1])
            globals.report.drawString(185, 650, items[2])
            globals.report.drawString(245, 650, items[3])
            globals.report.drawString(330, 650, items[4])
            globals.report.drawString(390, 650, items[5])
            globals.report.drawString(480, 650, items[6])
            globals.report.line(35, 645, 525, 645)

            x = 55
            y = 630
            for record in records:
                if y <= 90:
                    globals.report.setFont("Helvetica-Oblique", 8)
                    globals.report.drawString(450, 75, "Página siguiente...")
                    globals.report.showPage()
                    self.footer(titulo)
                    self.topreport(titulo)
                    y = 630

                globals.report.setFont("Helvetica", 8)
                dni = '***' + record[0][4:7] + '***'
                globals.report.drawCentredString(x + 10, y, dni)
                globals.report.drawString(x + 50, y, str(record[2]))
                globals.report.drawString(x + 120, y, str(record[3]))
                globals.report.drawCentredString(x + 210, y, str(record[5]))
                globals.report.drawString(x + 280, y, str(record[8]))
                globals.report.drawString(x + 350, y, str(record[9]))
                globals.report.drawString(x + 430, y, "Activo" if str(record[10]) == 'True' else "Baja")
                y -= 25

            globals.report.save()
            os.startfile(pdf_path)

        except Exception as error:
            print("error en reportCustomers", error)

    def reportProducts(self):
        try:
            data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            namereporpro = data + "_reportproducts.pdf"
            pdf_path = os.path.join(self.rootPath, namereporpro)
            globals.report = canvas.Canvas(pdf_path)

            titulo = "Product List"
            self.footer(titulo)
            self.topreport(titulo)

            records = Conexion.listProducts(None)
            if not records:
                print("No Productos")
                return

            items = ["ID", "NAME", "FAMILY", "STOCK", "PRICE"]
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(60, 650, items[0])
            globals.report.drawString(165, 650, items[1])
            globals.report.drawString(310, 650, items[2])
            globals.report.drawString(390, 650, items[3])
            globals.report.drawString(480, 650, items[4])
            globals.report.line(35, 645, 525, 645)

            x = 55
            y = 630
            for record in records:
                if y <= 90:
                    globals.report.showPage()
                    self.footer(titulo)
                    self.topreport(titulo)
                    y = 630

                globals.report.setFont("Helvetica", 8)
                globals.report.drawCentredString(x + 10, y, str(record[0]))
                globals.report.drawString(x + 110, y, str(record[1]))
                globals.report.drawString(x + 255, y, str(record[2]))
                globals.report.drawString(x + 350, y, str(record[3]))
                globals.report.drawRightString(x + 450, y, str(record[4]))
                y -= 25

            globals.report.save()
            os.startfile(pdf_path)

        except Exception as error:
            print("error en reportProducts", error)

    def ticket(self):
        try:
            data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            ticket_name = data + "_ticket.pdf"
            pdf_path = os.path.join(self.rootPath, ticket_name)
            globals.report = canvas.Canvas(pdf_path)

            dni = globals.ui.txtDnifac.text()
            titulo = "FACTURA SIMPLIFICADA" if dni == "00000000T" else "FACTURA"
            records = Conexion.dataOneCustomer(dni)

            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(220, 700, "DNI: " + str(records[0]))
            globals.report.drawString(220, 685, "APELLIDOS: " + str(records[2]))
            globals.report.drawString(220, 670, "NOMBRE: " + str(records[3]))
            globals.report.drawString(220, 655, "DIRECCIÓN: " + str(records[6]))
            globals.report.drawString(220, 640, "LOCALIDAD: " + str(records[8]) + "  PROVINCIA: " + str(records[7]))

            self.topreport(titulo)
            self.footer(titulo)
            globals.report.save()
            os.startfile(pdf_path)

        except Exception as error:
            print("error en ticket", error)
