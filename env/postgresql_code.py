import psycopg2

try:
    connection = psycopg2.connect(
        host='localhost',
        database='GoFiles',
        user='postgres',
        password='a1357'
    )
    print("Conexión exitosa")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Files")
    rows = cursor.fetchall()
    for row in rows:
        print(rows)


except Exception as ex:
    print(ex)

finally:
    connection.close()
    print("Conexión finalizada")