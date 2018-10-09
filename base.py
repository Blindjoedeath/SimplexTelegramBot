import sqlite3


def create_tables():
    with sqlite3.connect("base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

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
                           FOREIGN KEY(userId, resName) REFERENCES Resources(userId, name),
                           FOREIGN KEY(userId, prodName) REFERENCES Products(userId, name))
                       """)
        conn.commit()

create_tables()

class Base:
    @staticmethod
    def _insertObject(tableName, *values):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            valStr = "(" + "?, " * (len(values) - 1) + "?)"
            cursor.execute("INSERT INTO " + tableName +
                           " VALUES " + valStr, values)
            conn.commit()

    @staticmethod
    def _fetchObject(tableName, colName, userId):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            cursor.execute(" SELECT " + colName +
                           " FROM " + tableName +
                           " WHERE userId = ?", [userId])

            return cursor.fetchall()

    @staticmethod
    def insertResource(userId, resourse):
        Base._insertObject("Resources", userId, resourse.name, resourse.count)

    @staticmethod
    def insertProduct(userId, product):
        Base._insertObject("Products", userId, product.name, product.price)

    @staticmethod
    def insertConsumption(userId, consumption):
        Base._insertObject("ProductConsumptions", userId, consumption.product_name,
                            consumption.resource_name, consumption.resCons)

    @staticmethod
    def fetchResNames(userId):
        return Base._fetchObject("Products", "name", userId)

    @staticmethod
    def fetchProdNames(userId):
        return Base._fetchObject("Resources", "name", userId)

    @staticmethod
    def _checkDialog(userId):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            cursor.execute(""" SELECT COUNT(*)
                               FROM Dialogs
                               WHERE userId=?
                           """, [userId])
            if cursor.fetchall()[0][0] == 0:
                Base._insertObject("Dialogs", userId, 'DEFAULT')

    @staticmethod
    def getDialog(userId):
        Base._checkDialog(userId)
        return Base._fetchObject("Dialogs", "name", userId)[0][0]

    @staticmethod
    def setDialog(userId, dialog):
        Base._checkDialog(userId)
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            cursor.execute(" UPDATE Dialogs " +
                           " SET name = ? " +
                           " WHERE userId = ?", [dialog, userId])
