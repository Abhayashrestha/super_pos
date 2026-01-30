from core.model import Product
def get_connection():
    import psycopg2
    creds={"host":"localhost",
           "database":"",
           "user":"postgres",
           "password":""}

    try:
        connection=psycopg2.connect(**creds)
        connection.cursor()
        print("Connection successful")
        return connection

    except (Exception,psycopg2.Error) as error:
        print(f"{error} has occurred")

connect=get_connection()

def db_add_product(connection,product):
    try:
        with connection.cursor() as cur:
            sql_query='INSERT INTO products (name,price,quantity,category) VALUES (%s,%s,%s,%s)'
            insert_values= product.name,product.price,product.quantity,product.category
            cur.execute(sql_query,insert_values)
            connection.commit()
            print(f"Product:{product.name} has been added successfully")
    except Exception as e:
        connection.rollback()
        print(f"{e} error has occurred")
        return None


#db_add_product(connect,"Apple",10,100,"Fruit")

def db_delete_product(connection,p_id):
    try:
        with connection.cursor as cur:
            del_sql='DELETE FROM products where product_id=%s'
            cur.execute(del_sql,(p_id,))
            connection.commit()
            print (f'Product:{p_id} has been deleted successfully')
    except Exception as e:
        connection.rollback()
        print(f"{e}:Error has occurred")
        return None

def db_view_product(connection,p_id):
    try:
        with connection.cursor as cur:
            display_sql='SELECT product_id,name,price,quantity,category FROM products where product_id=%s'
            cur.execute(display_sql,(p_id,))
            items=cur.fetchone()
            if items:
                return Product(items[0],items[1],items[2],items[3],items[4])
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
            check_sql='SELECT product_id,price,quantity from products WHERE product_id=%s'
            stock_reduce_sql='UPDATE products SET quantity=quantity-%s WHERE product_id=%s'
            sales_sql='INSERT INTO sales (customer_name) VALUES (%s) RETURNING sale_id'
            sale_item_sql='INSERT INTO sale_item (product_id,sale_id,quantity,current_price) VALUES (%s,%s,%s,%s) returning*'
            cur.execute(check_sql,(product_id,))
            result = cur.fetchone()

            if not result:
                raise ValueError("Product Not Found")
            p_id,current_price,current_quantity=result

            if current_quantity>=quantity:
                cur.execute(stock_reduce_sql,(quantity,product_id))
                cur.execute(sales_sql,(customer_name,))
                s_id=cur.fetchone()[0]
                line_item=p_id,s_id,quantity,current_price
                cur.execute(sale_item_sql,line_item)
                connection.commit()
                return s_id

            else:
                raise ValueError("Sorry! We do not have that many in stock")

    except Exception as e:
        print(f"{e} error has occurred")
        connection.rollback()

c_name="bob"
sales_processing(connect,3,10,c_name)
