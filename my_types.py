class Resource:
    def __init__(self, name, count):
        self.name = name
        self.count = count


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Constrain:
    def __init__(self, product_name, resource_name, res_value):
        self.product_name = product_name
        self.resource_name = resource_name
        self.res_value = res_value