import globals
from PyQt6 import QtSql

class Conexion:
    @staticmethod
    def db_connect(filename):
        try:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filename)
            if not db.open():
                return False
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
                # Devuelve (Nombre, Precio)
                return (str(query.value(0)), float(query.value(1)))
            return None
        except Exception as e:
            print("Error selectProduct:", e)
            return None

    @staticmethod
    def insertInvoice(dni, fecha):
        try:
            query = QtSql.QSqlQuery()
            # En tu imagen: dninie y data
            query.prepare("INSERT INTO invoices (dninie, data) VALUES (:dni, :fecha)")
            query.bindValue(":dni", str(dni))
            query.bindValue(":fecha", str(fecha))
            return query.exec()
        except Exception as e:
            print("Error insertInvoice:", e)
            return False


    @staticmethod
    def allInvoices():
        try:
            query = QtSql.QSqlQuery()
            # En tu imagen: idfac, dninie, data
            query.prepare("SELECT idfac, dninie, data FROM invoices ORDER BY idfac DESC")
            lista = []
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(3)]
                    lista.append(row)
            return lista
        except Exception as e:
            print("error allInvoices", e)
            return []

    @staticmethod
    def addPro(newpro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO Products (Code, Name, Family, Stock, \"Unit Price\") VALUES (:code, :name, :family, :stock, :price)")
            query.bindValue(":code", newpro[0]); query.bindValue(":name", newpro[1])
            query.bindValue(":family", newpro[2]); query.bindValue(":stock", newpro[3])
            query.bindValue(":price", newpro[4])
            return query.exec()
        except Exception as e:
            return False

    @staticmethod
    def modifPro(datosPro):
        try:
            query = QtSql.QSqlQuery()
            # IMPORTANTE: Usamos comillas dobles para "Unit Price" por el espacio
            query.prepare("""
                    UPDATE Products 
                    SET Name = :name, 
                        Stock = :stock,
                        Family = :family, 
                        "Unit Price" = :price 
                    WHERE Code = :code
                """)

            # Vinculamos los valores asegurando que el tipo de dato sea correcto
            query.bindValue(":code", int(datosPro[0]))  # El código debe ser entero
            query.bindValue(":name", str(datosPro[1]))
            query.bindValue(":family", str(datosPro[2]))
            query.bindValue(":stock", int(datosPro[3]))  # El stock debe ser entero
            query.bindValue(":price", str(datosPro[4]))  # El precio se guarda como texto según tu BD

            if query.exec():
                return True
            else:
                print("Error SQL en modifPro:", query.lastError().text())
                return False
        except Exception as e:
            print("Error en modifPro (conexion.py):", e)
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
            query = QtSql.QSqlQuery("SELECT Code, Name, Family, Stock, \"Unit Price\" FROM Products ORDER BY Name")
            while query.next():
                row = [query.value(i) for i in range(5)]
                records.append(row)
            return records
        except Exception as e:
            return []

    @staticmethod
    def dataOneProduct(nombre):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT Code, Name, Family, Stock, \"Unit Price\" FROM Products WHERE Name = :name")
            query.bindValue(":name", nombre)
            if query.exec() and query.next():
                return [query.value(i) for i in range(5)]
            return None
        except Exception as e:
            return None

    @staticmethod
    def dataOneCustomer(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE mobile = :dato OR dni_nie = :dato")
            query.bindValue(":dato", dni)
            if query.exec() and query.next():
                return [query.value(i) for i in range(query.record().count())]
            return None
        except Exception as e:
            return None

    @staticmethod
    def listProv():
        records = []
        query = QtSql.QSqlQuery("SELECT provincia FROM provincias ORDER BY provincia")
        while query.next():
            records.append(query.value(0))
        return records

    @staticmethod
    def listMuniProv(provincia):
        records = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT municipio FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = :prov) ORDER BY municipio")
        query.bindValue(":prov", provincia)
        if query.exec():
            while query.next():
                records.append(query.value(0))
        return records

    @staticmethod
    def deleteCli(dni):
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
        try:
            query = QtSql.QSqlQuery()
            # En tu imagen la tabla sales tiene: idv, idfac, idpro, amount
            query.prepare("INSERT INTO sales (idfac, idpro, amount) VALUES (:idfac, :idpro, :qty)")
            query.bindValue(":idfac", int(venta[0]))
            query.bindValue(":idpro", int(venta[1]))
            query.bindValue(":qty", int(venta[2]))
            return query.exec()
        except Exception as e:
            print("Error insertVenta:", e)
            return False


    @staticmethod
    def deleteVentasFactura(id_factura):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM sales WHERE idFactura = :id")
        query.bindValue(":id", id_factura)
        query.exec()

    @staticmethod
    def getVentas(id_factura):
        lista = []
        query = QtSql.QSqlQuery()
        # El JOIN es vital para traer el Nombre y el Precio que no están en la tabla 'sales'
        query.prepare("""
                SELECT s.idv, s.idpro, p.Name, p."Unit Price", s.amount, (s.amount * p."Unit Price") 
                FROM sales as s 
                INNER JOIN Products as p ON s.idpro = p.Code 
                WHERE s.idfac = :id
            """)
        query.bindValue(":id", id_factura)
        if query.exec():
            while query.next():
                # Guardamos: [id_venta, id_prod, nombre, precio, cantidad, total_linea]
                row = [query.value(0), query.value(1), query.value(2),
                       float(query.value(3)), int(query.value(4)), float(query.value(5))]
                lista.append(row)
        return lista

    @staticmethod
    def modifcli(dni, modifcli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("""UPDATE customers SET adddata=:alta, surname=:apel, name=:nome, mail=:mail, 
                          mobile=:movil, address=:dir, province=:prov, city=:muni, historical=:estado, invoicetype=:fact 
                          WHERE dni_nie=:dni""")
            query.bindValue(":dni", dni); query.bindValue(":alta", modifcli[1])
            query.bindValue(":apel", modifcli[2]); query.bindValue(":nome", modifcli[3])
            query.bindValue(":mail", modifcli[4]); query.bindValue(":movil", modifcli[5])
            query.bindValue(":dir", modifcli[6]); query.bindValue(":prov", modifcli[7])
            query.bindValue(":muni", modifcli[8]); query.bindValue(":estado", str(modifcli[9]))
            query.bindValue(":fact", modifcli[10])
            return query.exec()
        except Exception: return False

    @staticmethod
    def addCli(newcli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("""INSERT INTO customers (dni_nie, adddata, surname, name, mail, mobile, address, province, city, invoicetype, historical) 
                          VALUES (:dni, :alta, :apel, :nome, :mail, :movil, :dir, :prov, :muni, :fact, :estado)""")
            query.bindValue(":dni", newcli[0]); query.bindValue(":alta", newcli[1])
            query.bindValue(":apel", newcli[2]); query.bindValue(":nome", newcli[3])
            query.bindValue(":mail", newcli[4]); query.bindValue(":movil", newcli[5])
            query.bindValue(":dir", newcli[6]); query.bindValue(":prov", newcli[7])
            query.bindValue(":muni", newcli[8]); query.bindValue(":fact", newcli[9])
            query.bindValue(":estado", "True")
            return query.exec()
        except Exception: return False

    @staticmethod
    def deletePro(codigo):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM Products WHERE Code = :code")
        query.bindValue(":code", codigo)
        return query.exec()

    @staticmethod
    def deleteInvoice(id_factura):
        try:
            # 1. Borramos primero las ventas asociadas a esa factura
            queryVentas = QtSql.QSqlQuery()
            queryVentas.prepare("DELETE FROM sales WHERE idfac = :id")
            queryVentas.bindValue(":id", id_factura)
            queryVentas.exec()

            # 2. Borramos la factura
            queryFac = QtSql.QSqlQuery()
            queryFac.prepare("DELETE FROM invoices WHERE idfac = :id")
            queryFac.bindValue(":id", id_factura)

            return queryFac.exec()
        except Exception as e:
            print("Error en deleteInvoice:", e)
            return False

    @staticmethod
    def deleteVenta(id_venta):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM sales WHERE idv = :idv")
            query.bindValue(":idv", int(id_venta))
            return query.exec()
        except Exception as e:
            print("Error en deleteVenta SQL:", e)
            return False

    @staticmethod
    def dataOneProduct_by_Code(codigo):
        query = QtSql.QSqlQuery()
        query.prepare("SELECT Code, Name, Family, Stock, \"Unit Price\" FROM Products WHERE Code = :code")
        query.bindValue(":code", str(codigo))
        if query.exec() and query.next():
            return [query.value(i) for i in range(5)]
        return None