from core.model import Product, LineItem, Sale

apple=Product("001",'Apple',0.5)
order_1=LineItem(apple,4)
my_receipt=Sale('01')
my_receipt.add_item(order_1)
print(my_receipt)

