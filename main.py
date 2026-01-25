from core.model import Product, LineItem, Sale
from core.engine import Catalog

apple=Product("001",'Apple',0.5,5)
banana=Product("002",'Banana',10,5)

order_1=LineItem(apple,4)
my_receipt=Sale('01')
my_receipt.add_item(order_1)
find=Catalog()
print(find.add_product(banana))
print(find.add_product(apple))
print(find.search_product("002"))
valid=find.check_stock("001",4)
print(find.withdraw_stock('001',4))

find.display_product()






