from core.model import Product, LineItem, Sale
from core.engine import Catalog

def role():
    print("|Press 1 for admin|")
    print("|Press 2 for customer|")
    user=int(input("Please Enter your role"))
    if user==1:
        admin()
    elif user==2:
        costumer()
    else:
        print("Please select from the option")

def admin():
    print("|Press 1 to add product| ")
    print("|Press 2 to delete product| ")
    print("|Press 3 to display product| ")
    print("Press 4 to find product| ")
    option=int(input("Enter your choice"))
    if option==1:
        p_id=input("Please enter the id of the product| ")
        p_name=input("Please enter the name of the product| ")
        p_price=int(input("Please enter the price of the product| "))
        p_quantity=int(input("Please enter the number of product| "))
        p_category=input("Please enter the category of product| ")
    elif option==2:
        p_id=input("Please enter the id of the product you wish to delete: ")
    elif option==3:
        pass
    elif option==4:
        p_id=input("|Please enter id of the product you wish to find| ")
    else:
        print("Please enter a valid option")

def costumer():
    print("Press 1 to view product")
    print("Press 2 to find product")
    print("Press 3 to buy product")
    option=int(input("Enter your choice"))
    if option==1:
        pass
    elif option==2:
        p_id = input("|Please enter id of the product you wish to find| ")
    elif option==3:
        p_id = input("|Please enter id of the product you wish to buy| ")
        p_quantity=int(input("Please enter the number of product| "))
    else:
        print("Please enter a valid option")


def main():
    program=Catalog()
    is_running=True
    while is_running:
        role()

main()










