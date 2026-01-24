from core.model import Product, LineItem, Sale
from core.engine import Catalog

apple=Product("001",'Apple',0.5)
order_1=LineItem(apple,4)
my_receipt=Sale('01')
my_receipt.add_item(order_1)
find=Catalog()
find.add_product(apple)
print(find.search_product("001"))


def role():
    print("----------------------------")
    print("Press 1 for admin")
    print("Press 2 for customer")
    try:
        first=int(input("Press any key to continue"))
        if first not in [1,2]:
            print("Please enter 1 or 2")
        return first
    except ValueError:
        print("Please enter a number")

def admin():
    print("Press 1 to add product")
    print("Press 2 to delete product")
    print("Press 3 to view product")
    print("Press 4 to modify product")
    try:
        ad=int(input("Press any key to continue"))
        if ad==1:
            p_id=input("Please enter product_id")
            p_name=input("Please enter product name")
            p_price=input("Please enter product price")
            p_quantity=input("Please enter product quantity")
            product=Product(p_id,p_name,p_price)
            line_item=LineItem(product,p_quantity)
            print(line_item)

        if ad not in [1,2,3,4]:
            print("Please enter from the options")
    except ValueError:
        print("Please enter a number")

def customer():
    print("Press 1 to view product")
    print("Press 2 to buy product")
    print("Press 3 to find product")
    try:
        cu=int(input("Press any key to continue"))
        if cu not in [1,2]:
            print("Please enter from the options")
            return cu
    except ValueError:
        print("Please enter a number")




is_running=True
while is_running:
    role()
    if role()==1:
        admin()
    elif role()==2:
        customer()




