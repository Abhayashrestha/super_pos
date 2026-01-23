from .model import Product

class Catalog:
    def __init__(self):
        self.catalog=[]
    def add_product(self,product_instance):
        self.catalog.append(product_instance)

