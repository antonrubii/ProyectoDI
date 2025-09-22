import events
import globals
from dlgCalendar import *
from datetime import datetime

class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        globals.vencal = Ui_dlgCalendar()
        globals.vencal.setupUi(self)
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        globals.vencal.Calendar.setSelectedDate((QtCore.QDate(year, month, day)))
        globals.vencal.Calendar.clicked.connect(events.Events.loadData)