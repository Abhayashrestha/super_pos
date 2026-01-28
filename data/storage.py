def get_connection():
    import psycopg2
    creds={"host":"",
           "database":"",
           "user":"",
           "password":""}

    try:
        connection=psycopg2.connect(**creds)
        connection.cursor()
        return connection

    except (Exception,psycopg2.Error) as error:
        print(f"{error} has occurred")
