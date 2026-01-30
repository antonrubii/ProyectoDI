import sqlite3
import globals
from PyQt6 import QtSql


class Conexion:

    @staticmethod
    def db_connect(filename):
        try:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filename)
            if not db.open():
                print("Error en la conexión")
                return False
            else:
                print("Conexión exitosa")
                return True
        except Exception as e:
            print("Ocurrió un error en la conexión:", e)
            return False

    @staticmethod
    def selectProduct(code):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT Name, \"Unit Price\" FROM Products WHERE Code = :code")
            query.bindValue(":code", code)
            if query.exec() and query.next():
                return (query.value(0), query.value(1))
            return ("", 0)
        except Exception as e:
            print("Error selectProduct", e)
            return ("", 0)

    @staticmethod
    def insertInvoice(dni, fecha):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices (dni, fecha) VALUES (:dni, :fecha)")
            query.bindValue(":dni", dni)
            query.bindValue(":fecha", fecha)
            return query.exec()
        except Exception as e:
            print("error insertInvoice", e)
            return False

    @staticmethod
    def allInvoices():
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT id, dni, fecha FROM invoices ORDER BY id DESC")
            lista = []

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    lista.append(row)

            return lista

        except Exception as e:
            print("error allInvoices", e)
            return []

    @staticmethod
    def addPro(newcli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("""
                INSERT INTO Products (Code, Name, Family, Stock, "Unit Price")
                VALUES (:code, :name, :family, :stock, :price)
            """)

            query.bindValue(":code", newcli[0])
            query.bindValue(":name", newcli[1])
            query.bindValue(":family", newcli[2])
            query.bindValue(":stock", newcli[3])
            query.bindValue(":price", newcli[4])

            return query.exec()

        except Exception as e:
            print("error en addPro:", e)
            return False

    @staticmethod
    def dataOneProduct(code):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM Products WHERE Code = :code")
            query.bindValue(":code", code)

            if query.exec() and query.next():
                record = query.record()
                data = []
                for i in range(record.count()):
                    data.append(query.value(i))
                return tuple(data)

            return None

        except Exception as e:
            print("Error en dataOneProduct:", e)
            return None

    @staticmethod
    def modifPro(modifcli):
        try:
            query = QtSql.QSqlQuery()

            query.prepare("""
                UPDATE Products 
                SET Code = :code_new,
                    Name = :name,
                    Family = :family,
                    Stock = :stock,
                    "Unit Price" = :price
                WHERE Code = :code_old
            """)

            query.bindValue(":code_old", modifcli[0])
            query.bindValue(":code_new", modifcli[0])
            query.bindValue(":name", modifcli[1])
            query.bindValue(":family", modifcli[2])
            query.bindValue(":stock", modifcli[3])
            query.bindValue(":price", modifcli[4])

            return query.exec()

        except Exception as e:
            print("Error modifPro:", e)
            return False

    @staticmethod
    def listCustomers(var):
        listCustomers = []
        query = QtSql.QSqlQuery()
        if var:
            query.prepare("SELECT * FROM customers where historical = :true order by surname;")
            query.bindValue(":true", "True")
        else:
            query.prepare("SELECT * FROM customers order by surname;")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                listCustomers.append(row)
        return listCustomers

    @staticmethod
    def listProducts():
        try:
            records = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM products")  # sacar filtro
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    records.append(row)
            return records
        except Exception as e:
            print("error selectProduct", e)
            return []

    @staticmethod
    def dataOneCustomer(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE dni_nie = :dni OR mobile = :dni")
            query.bindValue(":dni", dni)
            if query.exec() and query.next():
                return [query.value(i) for i in range(query.record().count())]
            return []
        except Exception as e:
            print("error en dataOneCustomer", e)
            return []

    @staticmethod
    def listProv():
        records = []
        query = QtSql.QSqlQuery("SELECT name FROM provinces ORDER BY name")
        while query.next():
            records.append(query.value(0))
        return records

    @staticmethod
    def listMuniProv(province):
        records = []
        query = QtSql.QSqlQuery()
        query.prepare(
            "SELECT name FROM municipalities WHERE province_id = (SELECT id FROM provinces WHERE name = :prov)")
        query.bindValue(":prov", province)
        if query.exec():
            while query.next():
                records.append(query.value(0))
        return records

    @staticmethod
    def deleteCli(dni):
        """ Borrado lógico: pone historical a False """
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE customers SET historical = 'False' WHERE dni_nie = :dni")
        query.bindValue(":dni", dni)
        return query.exec()

    @staticmethod
    def updateStock(codigo, cantidad):
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE Products SET Stock = Stock - :cant WHERE Code = :code")
        query.bindValue(":cant", float(cantidad))
        query.bindValue(":code", codigo)
        return query.exec()

    @staticmethod
    def insertVenta(venta):
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO sales (idFactura, idProducto, amount, total) VALUES (:idfac, :idpro, :qty, :total)")
        query.bindValue(":idfac", int(venta[0]))
        query.bindValue(":idpro", int(venta[1]))
        query.bindValue(":qty", float(venta[2]))
        query.bindValue(":total", float(venta[3]))
        return query.exec()

    @staticmethod
    def deleteVentasFactura(id_factura):
        """ Borra las líneas de venta asociadas a una factura """
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM sales WHERE idFactura = :id")
        query.bindValue(":id", id_factura)
        query.exec()


    @staticmethod
    def getVentas(id_factura):
        lista = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT s.id, s.idProducto, p.Name, p.\"Unit Price\", s.amount, s.total "
                      "FROM sales as s INNER JOIN Products as p ON s.idProducto = p.Code "
                      "WHERE s.idFactura = :id")
        query.bindValue(":id", id_factura)
        if query.exec():
            while query.next():
                lista.append([query.value(i) for i in range(query.record().count())])
        return lista






