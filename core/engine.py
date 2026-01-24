from .model import Product

class Catalog:
    def __init__(self):
        self.catalog=[]
    def add_product(self,product_instance):
        self.catalog.append(product_instance)

    def search_product(self,product_id):
        for item in self.catalog:
            if item.product_id==product_id:
                return item
        return None




