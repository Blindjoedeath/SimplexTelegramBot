class Resource:
    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __str__(self):
        return self.name + "    " + str(self.count)


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name + "    " + str(self.price)

class ConsumptionRow:
    def __init__(self, prodName, resName, resCons):
        self.prodName = prodName
        self.resName = resName
        self.resCons = resCons

    def __str__(self):
        return self.prodName + "    " + self.resName + "    " + str(self.resCons)

class Consumption:
    def __init__(self, product, resource, resCons):
        self.product = product
        self.resource = resource
        self.resCons = resCons

