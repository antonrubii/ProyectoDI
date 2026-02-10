import globals
from dlgCalendar import Ui_dlgCalendar
from dlgAbout import Ui_dlgAbout
from PyQt6 import QtWidgets, QtCore
from datetime import datetime
import events


class Calendar(QtWidgets.QDialog):
    """
    CLASE: Ventana de Calendario.
    QUÉ HACE: Gestiona la pequeña ventana emergente que muestra un calendario para elegir fechas.
    """

    def __init__(self):
        """
        MÉT0DO: Constructor del Calendario.
        QUÉ HACE: Inicializa la interfaz del calendario, marca el día de hoy por defecto y conecta el clic.
        PARA EL EXAMEN: Es la ventana que aparece al pulsar el botón del icono del calendario.
        """
        super(Calendar, self).__init__()
        globals.vencal = Ui_dlgCalendar()
        globals.vencal.setupUi(self)

        # Obtenemos la fecha actual del sistema
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        # Seleccionamos hoy en el calendario al abrirse
        globals.vencal.Calendar.setSelectedDate(QtCore.QDate(ano, mes, dia))

        # CONEXIÓN: Cuando el usuario hace clic en un día, se llama a loadData de events.py
        globals.vencal.Calendar.clicked.connect(events.Events.loadData)


class dlgAbout(QtWidgets.QDialog):
    """
    CLASE: Ventana "Acerca de".
    QUÉ HACE: Muestra una ventana con información del autor y la versión del programa.
    """

    def __init__(self):
        """
        MÉTO0DO: Constructor del About.
        QUÉ HACE: Carga el diseño y configura el botón de cerrar.
        PARA EL EXAMEN: Es una ventana modal (bloquea la principal hasta que se cierra).
        """
        super(dlgAbout, self).__init__()
        globals.about = Ui_dlgAbout()
        globals.about.setupUi(self)

        # CONEXIÓN: Al pulsar el botón de la ventana, se cierra usando el méto0do de events.py
        globals.about.btnCloseabout.clicked.connect(events.Events.closeAbout)


class FileDialogOpen(QtWidgets.QFileDialog):
    """
    CLASE: Selector de Archivos.
    QUÉ HACE: Abre la ventana estándar de Windows para elegir un archivo (para restaurar Backup).
    PARA EL EXAMEN: No necesita lógica extra, se usa directamente invocando sus métodos heredados.
    """

    def __init__(self):
        super(FileDialogOpen, self).__init__()