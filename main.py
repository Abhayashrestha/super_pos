from core.model import Product, LineItem, Sale
from core.engine import Catalog


def add_product(catalog):
    p_id = input("Please enter the id of the product| ").strip().lower()
    p_name = input("Please enter the name of the product| ")
    p_price ="Please enter the price of the product|"
    p_price_val = integer_validation(p_price, 0, 999)
    p_quantity = "Please enter the number of product| "
    p_quantity_val = integer_validation(p_quantity, 0, 999)
    p_category = input("Please enter the category of product| ")
    product_instance=Product(p_id,p_name,p_price_val,p_quantity_val,p_category)
    catalog.add_product(product_instance)


def delete_product(catalog):
    p_id = input("Please enter the id of the product you wish to delete: ").strip().lower()
    catalog.delete_product(p_id)

def display_product(catalog):
    catalog.display_product()

def find_product(catalog):
    p_id=input("|Please enter id of the product you wish to find| ").strip().lower()
    catalog.search_product(p_id)

def buy_product(catalog):
    p_id=input("|Please enter id of the product you wish to buy| ").strip().lower()
    quantity="|Please enter the number of products you wish to buy"
    quantity_val=integer_validation(quantity,0,99)
    purchase=catalog.purchase_processing(p_id,quantity_val)


def termination(catalog):
    print( "Thank you for using the software we hope to see you soon| Goodbye")
    return False

def handle_invalid(catalog):
    print("Sorry please enter from the listed options: ")

def integer_validation(prompt,min_val,max_val):
    while True:
        try:
            value=int(input(prompt))
            if min_val < value < max_val:
                return value
            print(f"Out of range ({min_val}-{max_val}).")
        except ValueError:
            print("Invalid input. Please enter a number.")



admin_options={
    "1":add_product,
    "2":delete_product,
    "3":display_product,
    "4":find_product,
    "5":termination
}


def admin(catalog):
    while True:
        print("|Press 1 to add product| ")
        print("|Press 2 to delete product| ")
        print("|Press 3 to display product| ")
        print("Press 4 to find product| ")
        print("|Press 5 to go back|")
        option=input("Enter your choice")
        action=admin_options.get(option,handle_invalid)
        result = action(catalog)
        if result == False:
            break

customer_options={
    "1":display_product,
    "2":find_product,
    "3":buy_product,
    "4":termination
}

def costumer(catalog):
    while True:
        print("Press 1 to view product")
        print("Press 2 to find product")
        print("Press 3 to buy product")
        print("Press 4 to go back")
        option=input("Enter your choice")
        action=customer_options.get(option,handle_invalid)
        result = action(catalog)
        if result == False:
            break


role_options={
    "1":admin,
    "2":costumer,
    "3":termination
}

def menu(catalog):
    while True:
        print("|Press 1 for admin|")
        print("|Press 2 for customer|")
        print("|Press 3 to go exit|")
        user = input("Please Enter your role")
        action = role_options.get(user, handle_invalid)
        result=action(catalog)
        if result==False:
            break


def main():
    catalog=Catalog()
    menu(catalog)


main()










