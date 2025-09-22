from dlgCalendar import *
from datetime import datetime
import globals


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        globals.vencal = Ui_dlgCalendar()
        globals.vencal.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        globals.vencal.Calendar.setSelectedDate((QtCore.QDate(ano, mes, dia)))
        globals.vencal.Calendar.clicked.connect(eventos.Eventos.cargaFecha)