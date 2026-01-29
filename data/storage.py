
def get_connection():
    import psycopg2
    creds={"host":"localhost",
           "database":"",
           "user":"",
           "password":""}

    try:
        connection=psycopg2.connect(**creds)
        connection.cursor()
        print("Connection successful")
        return connection

    except (Exception,psycopg2.Error) as error:
        print(f"{error} has occurred")

connect=get_connection()

def add_product(connection,name,price,quantity,category):
    try:
        with connection.cursor() as cur:
            sql_query='INSERT INTO products (name,price,quantity,category) VALUES (%s,%s,%s,%s)'
            insert_values= name,price,quantity,category
            cur.execute(sql_query,insert_values)
            connection.commit()
            print(f"Product:{name} has been added successfully")
    except Exception as e:
        connection.rollback()
        print(f"{e} error has occurred")
    finally:
        cur.close()

add_product(connect,"Apple",10,100,"Fruit")


