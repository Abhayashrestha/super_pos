from core.model import Product
from core.engine import Catalog
from data import storage


connect=storage.get_connection()
try:
    def add_product(catalog):
        p_name = input("Please enter the name of the product| ")
        p_price ="Please enter the price of the product|"
        p_price_val = integer_validation(p_price, 0, 999)
        p_quantity = "Please enter the number of product| "
        p_quantity_val = integer_validation(p_quantity, 0, 999)
        p_category = input("Please enter the category of product| ")
        product_instance=Product(p_name,p_price_val,p_quantity_val,p_category)
        new_product=catalog.add_product(product_instance)
        return new_product


    def delete_product(catalog):
        p_id = "Please enter the id of the product you wish to delete: "
        v_id = integer_validation(p_id, 0, 999)
        final=catalog.delete_product(v_id)
        if final:
            print(final)
        else:
            print("Product Not found")
        return None


    def display_product(catalog):
        view=catalog.display_product()
        if view:
            print(f"\n{'ID':<5} | {'Name':<15} | {'Price':<10} | {'Category':<9}| {'number':<5}")
            print("-" * 55)
            for item in view:
                print(f"{item['product_id']:<5} | {item['name']:<15} | ${item['price']:<9} | {item['category']:<9}| {item['quantity']:<5}")
            print("-" * 55 + "\n")
        else:
            print("\n[!] The catalog is currently empty.\n")


    def find_product(catalog):
        p_id="|Please enter id of the product you wish to find| "
        v_id = integer_validation(p_id, 0, 999)
        view=catalog.search_product(v_id)
        if view:
            print(f"\n--- Product Details ---")
            print(f"Name:     {view.name}")
            print(f"Price:    ${view.price}")
            print(f"Category: {view.category}")
            print(f"----------------------\n")
        else:
            print(f"\n[!] ID {v_id} not found in database.\n")


    def buy_product(catalog):
        p_id="|Please enter id of the product you wish to buy| "
        v_id = integer_validation(p_id, 0, 999)
        quantity="|Please enter the number of products you wish to buy"
        user_name=input('Please enter your user name')
        quantity_val=integer_validation(quantity,0,99)
        try:
            sale_result=catalog.purchase_processing(v_id,quantity_val,user_name)
            print(sale_result)
            if sale_result:
                receipt=input('press enter to print receipt| Anything else to exit')
                if receipt=='':
                    total_receipt=catalog.receipt_processing(sale_result)
                    print(total_receipt)


        except Exception as e:
            print(f"{e}Purchase Unsuccessful")
        return None


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
        catalog=Catalog(connect)
        menu(catalog)

    main()

finally:
    connect.close()













