import sqlite3


def create_tables():
    with sqlite3.connect("base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Resources
                          (userId INT NOT NULL,
                           resName TEXT NOT NULL,
                           value INT NOT NULL,
                           PRIMARY KEY(userId, resName))
                       """)
        conn.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS ProductConstrains
                          (userId INT NOT NULL,
                           prodName TEXT NOT NULL,
                           resName TEXT NOT NULL,
                           resValue INT NOT NULL,
                           PRIMARY KEY(userId, prodName, resName),
                           FOREIGN KEY(userId, resName) REFERENCES Resources(userId, resName),
                           FOREIGN KEY(userId, prodName) REFERENCES Products(userId, prodName))
                       """)
        conn.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Products
                          (userId INT NOT NULL,
                           prodName TEXT NOT NULL,
                           price INT NOT NULL,
                           PRIMARY KEY(userId, prodName))
                       """)
        conn.commit()
create_tables()


class Base:
    @staticmethod
    def insert_resource(userId, resourse):
        with sqlite3.connect("base.db") as conn:
            conn.cursor().execute("""INSERT INTO Resources
                              VALUES (?, ?, ?)
                           """, [userId, resourse.name, resourse.count])
            conn.commit()

    @staticmethod
    def insert_product(userId, product):
        with sqlite3.connect("base.db") as conn:
            conn.cursor().execute("""INSERT INTO Products
                              VALUES (?, ?, ?)
                           """, [userId, product.name, product.price])
            conn.commit()

    @staticmethod
    def insert_constrain(userId, constrain):
        with sqlite3.connect("base.db") as conn:
            conn.cursor().execute("""INSERT INTO ProductConstrains
                               VALUES (?, ?, ?, ?)
                            """, [userId,
                                  constrain.product_name,
                                  constrain.resource_name,
                                  constrain.res_value])
            conn.commit()

    @staticmethod
    def fetch_res_names(userId):
        with sqlite3.connect("base.db") as conn:
            conn.cursor().execute("""SELECT prodName FROM Products
                                     WHERE userId=?
                                   """, [userId])

            print(len(conn.cursor().fetchall()))

            return conn.cursor().fetchall()

    @staticmethod
    def fetch_prod_names(userId):
        with sqlite3.connect("base.db") as conn:
            conn.cursor().execute("""SELECT resName FROM Resources
                              WHERE userId=?
                           """, [userId])
            return conn.cursor().fetchall()
