import sqlite3
from my_types import Resource, Product, ConsumptionRow, Consumption

def create_tables():
    with sqlite3.connect("base.db") as conn:
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Dialogs
                          (userId INT NOT NULL,
                           name TEXT NOT NULL DEFAULT 'start',
                           PRIMARY KEY(userId))
                       """)

        conn.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Resources
                          (userId INT NOT NULL,
                           name TEXT NOT NULL,
                           value INT NOT NULL,
                           PRIMARY KEY(userId, name))
                       """)
        conn.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Products
                          (userId INT NOT NULL,
                           name TEXT NOT NULL,
                           price INT NOT NULL,
                           PRIMARY KEY(userId, name))
                       """)
        conn.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ProductConsumptions
                          (userId INT NOT NULL,
                           prodName TEXT NOT NULL,
                           resName TEXT NOT NULL,
                           resValue INT NOT NULL,
                           PRIMARY KEY(userId, prodName, resName),
                           FOREIGN KEY(userId, resName) REFERENCES Resources(userId, name) ON DELETE CASCADE,
                           FOREIGN KEY(userId, prodName) REFERENCES Products(userId, name) ON DELETE CASCADE)
                       """)
        conn.commit()

create_tables()

class Base:
    @staticmethod
    def _insertObject(tableName, values):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()

            cursor.execute("PRAGMA foreign_keys = ON")

            valStr = "(" + "?, " * (len(values) - 1) + "?)"
            cursor.execute("INSERT INTO " + tableName +
                           " VALUES " + valStr, values)
            conn.commit()

    @staticmethod
    def _deleteObject(tableName, colNames, colValues):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            valStr = map(lambda x: x + ' = ?', colNames)

            cursor.execute(" DELETE FROM " + tableName +
                           " WHERE " + ' AND '.join(valStr), colValues)
            conn.commit()

    @staticmethod
    def _fetchObject(tableName, userId, colNames, where = ''):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            cursor.execute(" SELECT " + ', '.join(colNames) +
                           " FROM " + tableName +
                           " WHERE " + where + "userId = ?", [userId])

            return cursor.fetchall()

    @staticmethod
    def insertResource(userId, resourse):
        Base._insertObject("Resources", [userId, resourse.name, resourse.count])

    @staticmethod
    def insertProduct(userId, product):
        Base._insertObject("Products", [userId, product.name, product.price])

    @staticmethod
    def insertConsumption(userId, consumption):
        Base._insertObject("ProductConsumptions", [userId, consumption.prodName,
                                                   consumption.resName, consumption.resCons])

    @staticmethod
    def fetchResources(userId):
        return [Resource(x[0], x[1]) for x in Base._fetchObject("Resources", userId, ["name", "value"])]

    @staticmethod
    def fetchProducts(userId):
        return [Product(x[0], x[1]) for x in Base._fetchObject("Products", userId, ["name", "price"])]

    @staticmethod
    def fetchConsumptionRows(userId):
        return [ConsumptionRow(x[0], x[1], x[2]) for x in Base._fetchObject("ProductConsumptions", userId, ["prodName",
                                                                            "resName", "resValue"])]
    @staticmethod
    def fetchConsumptions(userId):
        return [Consumption(Product(x[0], x[1]), Resource(x[2], x[3]), x[4]) for x in
                Base._fetchObject("""ProductConsumptions
		                            LEFT Join Products On prodName = Products.name
		                            LEFT Join Resources On resName = Resources.name""",
                                    userId, ['prodName', 'Products.price', 'resName', 'Resources.value',  'resValue'],
                                    "ProductConsumptions.")]

    @staticmethod
    def deleteResource(userId, resName):
        Base._deleteObject('Resources', ['userId', 'name'], [userId, resName])

    @staticmethod
    def deleteProduct(userId, prodName):
        Base._deleteObject('Products', ['userId', 'name'], [userId, prodName])

    @staticmethod
    def deleteConsumptionRow(userId, prodName, resName):
        Base._deleteObject('ProductConsumptions', ['userId', 'prodName', 'resName'], [userId, prodName, resName])