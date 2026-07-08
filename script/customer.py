import random
import data.storage as storage
import time
from core.engine import Catalog




def bot_purchase():
    bot_name = ["piers", "john", "josh", "johny", "arthur",
                 "clav", "togi", "steve", "jake", "Finn"]
    quantity = [1, 2, 3, 4, 5, 6, 7]
    connection = storage.get_connection()
    engine = Catalog(connection)
    try:
        while True:
            product=engine.display_product()
            if not product:
                print("waiting for product")
                time.sleep(10)
                continue

            name=random.choice(bot_name)
            random_product=random.choice(product)
            qty=random.choice(quantity)
            p_id=random_product['product_id']
            number=qty
            basket={p_id:number}
            customer=name
            print(f"{customer} is trying to purchase {random_product['name']} (ID: {p_id})...")
            result=engine.purchase_processing(basket,customer)
            if result['status']=='success':
                print(f"  [SUCCESS] Sale ID: {result['s_id']}")
            else:
                print(f"  [MISSED] Logic: {result['message']}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nStopping simulation. Closing connection...")
    finally:
        connection.close()


if __name__ == "__main__":
    bot_purchase()










