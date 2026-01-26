from core.model import Product, LineItem, Sale
from core.engine import Catalog

cat=Catalog()
apple=Product("001",'apple',50,100,'fruit')
cat.add_product(apple)
cat.purchase_processing('001',50)
print(cat.sales_history)
print(cat.catalog['001'].quantity)





