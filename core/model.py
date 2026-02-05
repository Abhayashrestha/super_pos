from datetime import datetime
class Product:
    def __init__(self,name,price,quantity,category,p_id=None):
        self.p_id=p_id
        self.name=name
        self.price=float(price)
        self.quantity=int(quantity)
        self.category=category

    def __str__(self):
        return f"name={self.name},\n price={self.price} \n,quantity={self.quantity},\ncategory={self.category}\n has been added"

class LineItem:
    def __init__(self,product_instance,quantity):
        self.product_instance=product_instance
        self.quantity=quantity
        self.price_sold_at=product_instance.price

    def get_total_price(self):
        total_price=self.price_sold_at*self.quantity
        return total_price

    def __str__(self):
        return f"Product={self.product_instance.name},quantity={self.quantity},price={self.price_sold_at},total_price={self.get_total_price()}"


class Sale:
    def __init__(self,sale_id,name=None,time=None):
        self.sale_id=sale_id
        self.items=[]
        self.name=name
        self.time=time


    def add_item(self,item_to_add):
        self.items.append(item_to_add)

    def get_total_sales(self):
        total_sales=0
        for item in self.items:
            total_sales+=item.get_total_price()
        return total_sales

    def __str__(self):
        header = f"--- RECEIPT #{self.sale_id} ---\nCustomer: {self.name}\nDate: {self.time}\n"
        items_str = "\n".join([f"{item.product_instance.name:<15} x{item.quantity:<3} ${item.price_sold_at:>7.2f}" for item in self.items])
        footer = f"\n--------------------------\nTOTAL: ${self.get_total_sales():>15.2f}"
        return header + items_str + footer





