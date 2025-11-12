from reportlab.pdfgen import canvas
import os
import datetime
from PIL import Image
from conexion import *

class Reports():
    def __init__(self):
        rootPath = ".\\reports"
        data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.namereporcli = data + "_reportcustomers.pdf"
        self.pdf_path = os.path.join(rootPath, self.namereporcli)
        self.rootPath = rootPath
        self.c = canvas.Canvas(self.pdf_path)
        self.rootPath = rootPath

    def footer(self, titulo):
        try:
            self.c.line(35,50,525,50)
            day = datetime.datetime.today()
            day = day.strftime("%d/%m/%Y %H:%M:%S")
            self.c.setFont("Helvetica",size = 7)
            self.c.drawString(90,50, day)
            self.c.drawString(250,50,titulo)
            self.c.drawString(480, 50, str('Pagina : '+  self.c.getPageNumber()))

        except Exception as error :
            print(error)

    def topreport(self,titulo):
        try :
            path_logo  = '.\\img\\logo.ico'
            logo = Image.open(path_logo)
            if isinstance(logo,Image.Image):
                self.c.line(35,60,525,60)
                self.c.setFont('Helvetica-Bold',size = 10)
                self.c.drawString(55,785,"EMPRESA TEIS")
                self.c.drawCentredString(295,675,titulo)
                self.c.line(35,665,525,665)
                self.c.drawImage(path_logo,490,745,width=40,height=40)
                #datos de la empresa
                self.c.setFont('Helvetica',size = 9)
                self.c.drawString(55,755,"CIF : A13425258")
                self.c.drawString(55,745,"Avd. de Galicia ,101")
                self.c.drawString(55,735,"Vigo -36215 -España")
                self.c.drawString(55, 725, "Tlfo :986 123 456")
                self.c.drawString(55, 715, "email :teis@mail.com")
                self.c.line(50, 800, 160, 800)
                self.c.line(50, 695, 160, 695)
                self.c.line(50, 800, 50, 695)
                self.c.line(160, 800, 160, 695)


            else :
                print("no puedo cargar la imagen")

        except Exception as error:
            print("Error en topreport:", error)

    def reportCustomers(self):
        try:
            titulo = "lISTADO CLIENTES"
            self.footer(titulo)
            self.topreport(titulo)
            var = False
            records = Conexion.listCustomers(var)
            if not records:
                print("no customers found")
                return
            items = ["DNI_NIE","SURNAME","NAME","MOBILE","CITY","INVOICE TYPE","STATE"]
            self.c.setFont("Helvetica-Bold",  10)
            self.c.drawString(45, 650, str(items[0]))
            self.c.drawString(100, 650, str(items[1]))
            self.c.drawString(185, 650, str(items[2]))
            self.c.drawString(245, 650, str(items[3]))
            self.c.drawString(330, 650, str(items[4]))
            self.c.drawString(390, 650, str(items[5]))
            self.c.drawString(480, 650, str(items[6]))
            self.c.line(35,645,525,645)
            x = 55
            y = 630
            for record in records:
                if y <=90:  #crea una nueva pagina
                    self.c.setFont("Helvetica-Oblique", 8)
                    self.c.drawString(450, 75, "Pagina Siguiente...")
                    self.c.showPage() #crea una nueva pagina
                    self.footer(titulo)
                    self.topreport(titulo)
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
                    self.c.setFont("Helvetica-Bold", 10)
                    self.c.drawString(45, 650, str(items[0]))
                    self.c.drawString(105, 650, str(items[1]))
                    self.c.drawString(185, 650, str(items[2]))
                    self.c.drawString(245, 650, str(items[3]))
                    self.c.drawString(330, 650, str(items[4]))
                    self.c.drawString(390, 650, str(items[5]))
                    self.c.drawString(480, 650, str(items[6]))
                    self.c.line(35, 645, 525, 645)
                    x = 55
                    y = 630
                self.c.setFont("Helvetica", 8)
                dni ='***' + str(record[0][4:7]+'***')
                self.c.drawCentredString(x+10, y, dni)
                self.c.drawString(x+50, y, str(record[2]))
                self.c.drawString(x + 120, y, str(record[3]))
                self.c.drawCentredString(x + 210, y, str(record[5]))
                self.c.drawString(x + 280, y, str(record[8]))
                self.c.drawString(x + 350, y, str(record[9]))
                if str(record[10]) == 'True':
                    self.c.drawString(x + 430, y ,"Activo")
                else:
                    self.c.drawString(x + 430, y ,"Baja")
                y = y - 25
            self.c.save()
            for file in os.listdir(self.rootPath):
                if file.endswith(self.namereporcli):
                    os.startfile(self.pdf_path)

        except  Exception as error:
            print("error en reportCustomers",error)