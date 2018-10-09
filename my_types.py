class Resource:
    def __init__(self, name, count):
        self.name = name
        self.count = count


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ConsumptionRow:
    def __init__(self, product_name, resource_name, resCons):
        self.product_name = product_name
        self.resource_name = resource_name
        self.res_value = resCons

class Consumption:
    def __init__(self, product, resource, resCons):
        self.product = product
        self.resource = resource
        self.resCons = resCons
