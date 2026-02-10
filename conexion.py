import globals
from PyQt6 import QtSql, QtWidgets

class Conexion:

    # --- 1. CONEXIÓN ---
    @staticmethod
    def db_connect(filename):
        """QUÉ HACE: Abre el archivo SQLite. PARA EL EXAMEN: Es el motor. Si no hay conexión, no hay datos."""
        try:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filename)
            return db.open()
        except Exception as e:
            print("Error conexión:", e)
            return False

    # --- SECCIÓN CLIENTES (6 Métodos) ---
    @staticmethod
    def listCustomers(var):
        """QUÉ HACE: Trae todos los clientes. Si 'var' es True, filtra los que están de Alta."""
        listado = []
        query = QtSql.QSqlQuery()
        if var: query.prepare("SELECT * FROM customers WHERE historical = 'True' ORDER BY surname")
        else: query.prepare("SELECT * FROM customers ORDER BY surname")
        if query.exec():
            while query.next(): listado.append([query.value(i) for i in range(query.record().count())])
        return listado

    @staticmethod
    def dataOneCustomer(dni):
        """QUÉ HACE: Busca un cliente por DNI para rellenar el formulario al hacer click en la tabla."""
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM customers WHERE dni_nie = :d")
        query.bindValue(":d", dni)
        if query.exec() and query.next(): return [query.value(i) for i in range(query.record().count())]
        return None

    @staticmethod
    def addCli(newcli):
        """QUÉ HACE: Inserta un nuevo cliente (Botón Save)."""
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO customers (dni_nie, adddata, surname, name, mail, mobile, address, province, city, invoicetype, historical) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'True')")
        for dato in newcli: query.addBindValue(str(dato))
        return query.exec()

    @staticmethod
    def modifcli(dni, modifcli):
        """QUÉ HACE: Actualiza los datos de un cliente (Botón Modify)."""
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE customers SET adddata=?, surname=?, name=?, mail=?, mobile=?, address=?, province=?, city=?, historical=?, invoicetype=? WHERE dni_nie=?")
        for i in range(1, 11): query.addBindValue(str(modifcli[i]))
        query.addBindValue(dni)
        return query.exec()

    @staticmethod
    def deleteCli(dni):
        """QUÉ HACE: Baja lógica. Pone 'historical' a False (Botón Delete)."""
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE customers SET historical = 'False' WHERE dni_nie = :dni")
        query.bindValue(":dni", dni)
        return query.exec()

    @staticmethod
    def listProv():
        """QUÉ HACE: Llena el ComboBox de provincias."""
        lista = []
        query = QtSql.QSqlQuery("SELECT provincia FROM provincias")
        while query.next(): lista.append(query.value(0))
        return lista

    # --- SECCIÓN PRODUCTOS (6 Métodos) ---
    @staticmethod
    def listProducts():
        """QUÉ HACE: Carga la lista de almacén en la pestaña Products."""
        records = []
        query = QtSql.QSqlQuery("SELECT Code, Name, Family, Stock, \"Unit Price\" FROM Products ORDER BY Name")
        while query.next(): records.append([query.value(i) for i in range(5)])
        return records

    @staticmethod
    def selectProduct(code):
        """QUÉ HACE: Usado en VENTAS. Al poner el código, autocompleta Nombre y Precio."""
        query = QtSql.QSqlQuery()
        query.prepare("SELECT Name, \"Unit Price\" FROM Products WHERE Code = ?")
        query.addBindValue(code)
        if query.exec() and query.next(): return (str(query.value(0)), float(query.value(1)))
        return None

    @staticmethod
    def dataOneProduct(nombre):
        """QUÉ HACE: Busca un producto por Nombre."""
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM Products WHERE Name = ?")
        query.addBindValue(nombre)
        if query.exec() and query.next(): return [query.value(i) for i in range(5)]
        return None

    @staticmethod
    def dataOneProduct_by_Code(codigo):
        """QUÉ HACE: Busca producto por CÓDIGO. VITAL para el aviso de 'Solo quedan X peras'."""
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM Products WHERE Code = ?")
        query.addBindValue(codigo)
        if query.exec() and query.next(): return [query.value(i) for i in range(5)]
        return None

    @staticmethod
    def addPro(newpro):
        """QUÉ HACE: Crea un producto nuevo en Almacén."""
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO Products (Code, Name, Family, Stock, \"Unit Price\") VALUES (?, ?, ?, ?, ?)")
        for d in newpro: query.addBindValue(d)
        return query.exec()

    @staticmethod
    def modifPro(datos):
        """QUÉ HACE: Modifica un producto usando el código viejo para encontrarlo (WHERE code_old)."""
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE Products SET Code=?, Name=?, Family=?, Stock=?, \"Unit Price\"=? WHERE Code=?")
        for d in datos: query.addBindValue(d)
        return query.exec()

    @staticmethod
    def deletePro(codigo):
        """QUÉ HACE: Borrado físico de un producto de la base de datos."""
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM Products WHERE Code = ?")
        query.addBindValue(codigo)
        return query.exec()

    # --- SECCIÓN FACTURACIÓN Y VENTAS (9 Métodos) ---
    @staticmethod
    def insertInvoice(dni, fecha):
        """QUÉ HACE: Crea la cabecera de la factura (Botón Save de Invoicing)."""
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO invoices (dninie, data) VALUES (?, ?)")
        query.addBindValue(dni); query.addBindValue(fecha)
        return query.exec()

    @staticmethod
    def allInvoices():
        """QUÉ HACE: Carga la tabla de facturas de la izquierda."""
        lista = []
        query = QtSql.QSqlQuery("SELECT idfac, dninie, data FROM invoices ORDER BY idfac DESC")
        while query.next(): lista.append([str(query.value(i)) for i in range(3)])
        return lista

    @staticmethod
    def getVentas(id_factura):
        """QUÉ HACE: Trae las líneas de una factura con JOIN para sacar nombres y precios."""
        lista = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT s.idv, s.idpro, p.Name, p.\"Unit Price\", s.amount, (s.amount * p.\"Unit Price\") FROM sales as s INNER JOIN Products as p ON s.idpro = p.Code WHERE s.idfac = ?")
        query.addBindValue(id_factura)
        if query.exec():
            while query.next(): lista.append([query.value(i) for i in range(6)])
        return lista

    @staticmethod
    def insertVenta(venta):
        """QUÉ HACE: Guarda una línea de producto en la factura (Check Azul)."""
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO sales (idfac, idpro, amount) VALUES (?, ?, ?)")
        for d in venta: query.addBindValue(d)
        return query.exec()

    @staticmethod
    def deleteVenta(id_venta):
        """QUÉ HACE: Borra una sola línea de la factura (Papelera de la derecha)."""
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM sales WHERE idv = ?")
        query.addBindValue(id_venta)
        return query.exec()

    @staticmethod
    def deleteVentasFactura(id_factura):
        """QUÉ HACE: Borra todas las líneas de una factura (usado antes de borrar la factura)."""
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM sales WHERE idfac = ?")
        query.addBindValue(id_factura)
        return query.exec()

    @staticmethod
    def deleteInvoice(id_factura):
        """QUÉ HACE: Borra la cabecera de la factura (Papelera de la izquierda)."""
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM invoices WHERE idfac = ?")
        query.addBindValue(id_factura)
        return query.exec()

    @staticmethod
    def updateStock(codigo, cantidad):
        """QUÉ HACE: Resta las unidades vendidas del stock del almacén."""
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE Products SET Stock = Stock - ? WHERE Code = ?")
        query.addBindValue(cantidad); query.addBindValue(codigo)
        return query.exec()

    @staticmethod
    def listMuniProv(provincia):
        """QUÉ HACE: Llena el combo de ciudades filtrando por la provincia elegida."""
        lista = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT municipio FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = ?) ORDER BY municipio")
        query.addBindValue(provincia)
        if query.exec():
            while query.next(): lista.append(query.value(0))
        return lista