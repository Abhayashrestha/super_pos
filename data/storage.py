from core.model import Product,LineItem,Sale
def get_connection():
    import psycopg2
    creds={"host":"localhost",
           "database":"posdb",
           "user":"postgres",
           "password":"Shrestha#$1"}

    try:
        connection=psycopg2.connect(**creds)
        print("Connection successful")
        return connection

    except (Exception,psycopg2.Error) as error:
        print(f"{error} has occurred")


def db_add_product(connection,product):
    try:
        with connection.cursor() as cur:
            sql_query='''
            INSERT INTO products (name,price,quantity,category,image_path) 
            VALUES (%s,%s,%s,%s,%s) 
            ON CONFLICT (name) DO UPDATE 
            SET quantity = products.quantity + EXCLUDED.quantity,
            price = EXCLUDED.price,
            image_path = EXCLUDED.image_path;'''
            insert_values= product.name,product.price,product.quantity,product.category,product.image_path
            cur.execute(sql_query,insert_values)
            connection.commit()
            print(f"Product:{product.name} has been added successfully")
    except Exception as e:
        connection.rollback()
        print(f"{e} error has occurred")
        return None



def db_delete_product(connection,p_id):
    try:
        with connection.cursor() as cur:
            del_sql='DELETE FROM products where product_id=%s'
            cur.execute(del_sql,(p_id,))
            connection.commit()
            return f'Product:{p_id} has been deleted successfully'
    except Exception as e:
        connection.rollback()
        return f"{e}:Error has occurred"


def db_view_product(connection,p_id):
    try:
        with connection.cursor() as cur:
            display_sql='SELECT product_id,name,price,quantity,category FROM products where product_id=%s'
            cur.execute(display_sql,(p_id,))
            items=cur.fetchone()
            if items:
                return Product(items[1], items[2], items[3], items[4],items[0])

    except Exception as e:
        print(f"{e}:Error has occurred")
        return None


def db_view_all_product(connection):
    try:
        with connection.cursor() as cur:
            display=[]
            query="SELECT* FROM products"
            cur.execute(query)
            key= [column[0] for column in cur.description]
            for row in cur.fetchall():
                display.append(dict(zip(key,row)))
            return display


    except Exception as e:
        connection.rollback()
        print(f"{e} error has occurred")
        return None

#db_view_all_product(connect)

def sales_processing(connection,product_id,quantity,customer_name):
    try:
        with connection.cursor() as cur:
            check_sql='SELECT product_id,name,price,quantity,category from products WHERE product_id=%s'
            stock_reduce_sql='UPDATE products SET quantity=quantity-%s WHERE product_id=%s'
            sales_sql='INSERT INTO sales (customer_name) VALUES (%s) RETURNING sale_id'
            sale_item_sql='INSERT INTO sale_item (product_id,sale_id,quantity,current_price) VALUES (%s,%s,%s,%s) returning*'
            cur.execute(check_sql,(product_id,))
            result = cur.fetchone()



            if not result:
                raise ValueError("Product Not Found")
            p_id,product_name,current_price,current_quantity,product_category=result
            product_instance = Product(product_name, current_price, current_quantity, product_category, product_id)

            if current_quantity>=quantity:
                cur.execute(stock_reduce_sql,(quantity,product_id))
                cur.execute(sales_sql,(customer_name,))
                s_id=cur.fetchone()[0]
                line_item=p_id,s_id,quantity,current_price
                cur.execute(sale_item_sql,line_item)
                connection.commit()
                new_line_item=LineItem(product_instance,quantity)
                new_sale=Sale(s_id)
                new_sale.add_item(new_line_item)
                return s_id


            else:
                raise ValueError("Sorry! We do not have that many in stock")

    except Exception as e:
        print(f"{e} error has occurred")
        connection.rollback()


def db_get_receipt(connection,sale_id):
    try:
        with connection.cursor() as cur:
            sql='Select s.sale_id,p.name,si.quantity,si.Current_price,s.customer_name,s.created_at,p.quantity,p.category,p.product_id From sales s JOIN sale_item si on s.sale_id=si.sale_id LEFT JOIN products p on si.product_id=p.product_id WHERE s.sale_id=%s'
            cur.execute(sql,(sale_id,))
            out=cur.fetchall()
            if out:
                s_id=out[0][0]
                name,time=out[0][4],out[0][5]
                new_receipt = Sale(s_id,name,time)
                for item in out:
                    product_name,quantity,price,p_quantity,category,product_id=item[1],item[2],item[3],item[6],item[7],item[8]
                    product_instance=Product(product_name,price,p_quantity,category,product_id)
                    new_line_item=LineItem(product_instance,quantity)
                    new_receipt.add_item(new_line_item)
                return new_receipt


    except:
        raise ValueError("We could not find the sale")



