from .model import Product,Sale,LineItem

class Catalog:
    def __init__(self):
        self.catalog={}
        self.sales_history=[]

    def add_product(self,product_instance):
        if product_instance.product_id not in self.catalog:
            self.catalog[product_instance.product_id]=product_instance
            return  f'{product_instance.name} has been added'
        else:
            return f'{product_instance.product_id} has already been added'

    def search_product(self,product_id):
        if product_id in self.catalog:
            return self.catalog[product_id]
        return 'not found'


    def display_product(self):
        for product in self.catalog.values():
            print(product)


    def delete_product(self,product_id):
        if product_id in self.catalog:
            del self.catalog[product_id]


    def check_stock(self,product_id,requested_quantity):
        if product_id in self.catalog:
            if requested_quantity>self.catalog[product_id].quantity:
                return "no"
            return "yes"
        return 'product not found'


    def withdraw_stock(self,product_id,requested_quantity):
        valid=self.check_stock(product_id,requested_quantity)
        if valid=='yes':
            self.catalog[product_id].quantity-=requested_quantity
            return 'success'
        elif valid=='no':
            return 'Not Enough in stock'
        else:
            return 'Product not found'

    def purchase_processing(self, product_id, requested_quantity):
        in_stock = self.withdraw_stock(product_id, requested_quantity)

        if in_stock == 'success':
            target_product = self.catalog[product_id]
            new_item = LineItem(target_product, requested_quantity)
            s_id = len(self.sales_history) + 1
            new_sale = Sale(s_id)
            new_sale.add_item(new_item)
            self.sales_history.append(new_sale)
            return "Purchase has been made"

        elif in_stock == 'Not Enough in stock':
            return 'Sorry we do not have that many product in stock'
        else:
            # This handles 'Product not found' or anything else
            return 'Product not found'



















