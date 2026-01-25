from datetime import datetime
class Product:
    def __init__(self,product_id,name,price,quantity):
        self.product_id=product_id
        self.name=name
        self.price=float(price)
        self.quantity=int(quantity)

    def __repr__(self):
        return f"id={self.product_id},name={self.name},price={self.price},quantity={self.quantity}"

class LineItem:
    def __init__(self,product_instance,quantity):
        self.product_instance=product_instance
        self.quantity=quantity
        self.price_sold_at=product_instance.price

    def get_total_price(self):
        total_price=self.price_sold_at*self.quantity
        return total_price

    def __repr__(self):
        return f"Product={self.product_instance.name},quantity={self.quantity},price={self.price_sold_at},total_price={self.get_total_price()}"


class Sale:
    def __init__(self,sale_id):
        self.sale_id=sale_id
        self.timestamp = datetime.now()
        self.items=[]


    def add_item(self,item_to_add):
        self.items.append(item_to_add)

    def get_total_sales(self):
        total_sales=0
        for item in self.items:
            total_sales+=item.get_total_price()
        return total_sales

    def __repr__(self):
        return f"items={self.items} total_sales={self.get_total_sales()}"



