import sqlite3

conn = sqlite3.connect("base.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Resources
                  (userId INT NOT NULL,
                   resName TEXT NOT NULL,
                    value INT NOT NULL,
                    PRIMARY KEY(userId, resName))
               """)
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS ProductProperties
                  (userId INT NOT NULL,
                   prodName TEXT NOT NULL,
                   resName TEXT NOT NULL,
                   resValue INT NOT NULL,
                    PRIMARY KEY(userId, prodName, resName),
                    FOREIGN KEY(userId, resName) REFERENCES Resources(userId, resName))
               """)
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS ProductPrices
                  (userId INT NOT NULL,
                   prodName TEXT NOT NULL,
                   price INT NOT NULL,
                   PRIMARY KEY(userId, prodName),
                   FOREIGN KEY(userId, prodName) REFERENCES ProductProperties(userId, prodName))
               """)
conn.commit()


class Base:
    @staticmethod
    def insert_resource(userId, resourse):
        cursor.execute("""INSERT INTO Resources
                          VALUES ({0}, "{1}", {2})
                       """.format(userId, resourse.name, resourse.count))
        conn.commit()

    @staticmethod
    def insert_product(userId, product):
        for key, val in product.cost_norms.items():
            cursor.execute("""INSERT INTO ProductProperties
                              VALUES ({0}, "{1}", "{2}", {3})
                           """.format(userId, product.name, key, val))

            cursor.execute("""INSERT INTO ProductPrices
                              VALUES ({0}, "{1}", "{2}")
                           """.format(userId, product.name, product.price))
            conn.commit()

     #fetch methods





