import sqlite3


def create_tables():
    with sqlite3.connect("base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

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

        cursor.execute("""CREATE TABLE IF NOT EXISTS ProductConstrains
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
    def _insert_object(tableName, *values):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            valStr = "(" + "?, " * (len(values) - 1) + "?)"

            cursor.execute("INSERT INTO " + tableName +
                           " VALUES " + valStr, values)
            conn.commit()

    @staticmethod
    def _fetch_object(tableName, colName, userId):
        with sqlite3.connect("base.db") as conn:
            cursor = conn.cursor()
            cursor.execute(" SELECT " + colName +
                           " FROM " + tableName +
                           " WHERE userId = ?", [userId])

            return cursor.fetchall()

    @staticmethod
    def insert_resource(userId, resourse):
        Base._insert_object("Resources", userId, resourse.name, resourse.count)

    @staticmethod
    def insert_product(userId, product):
        Base._insert_object("Products", userId, product.name, product.price)

    @staticmethod
    def insert_constrain(userId, constrain):
        Base._insert_object("Products", userId, constrain.product_name,
                            constrain.resource_name, constrain.res_value)

    @staticmethod
    def fetch_res_names(userId):
        return Base._fetch_object("Products", "name", userId)

    @staticmethod
    def fetch_prod_names(userId):
        return Base._fetch_object("Resources", "name", userId)
