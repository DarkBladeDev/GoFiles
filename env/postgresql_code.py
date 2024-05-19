import psycopg2
from decouple import config

try:
    connection = psycopg2.connect(
        host=config('HOST'),
        database=config('DATABASE'),
        user=config('USER'),
        password=config('PASSWORD')
    )
    print("GoFIles (LOG) >> Conexión exitosa")


    def insertar_usuario():
        try:
            user = input("Username >> ")
            password = input("Password >> ")
            
            cursor = connection.cursor()
            cursor.execute("""
                            INSERT INTO public."Users"(
                            "Username", "Password")
                                VALUES (%s , %s);
                            """, (user, password))
            connection.commit()
            print("GoFIles (LOG) >> Usuario creado con exito")
            return True
        except Exception as ex:
            print("GoFIles (ERROR) >> ", ex)
            return False

    def eliminar_usuario():
        try:
            id = int(input("ID >> "))

            cursor = connection.cursor()
            cursor.execute("""
                            DELETE FROM public."Users"
                                WHERE "ID" = %s;
                            """, (id))
            print("GoFIles (LOG) >> Usuario borrado exitosamente!")
            return True
        except Exception as ex:
            print("GoFIles (ERROR) >> ", ex)
            return False
            
    def actualizar_usuario():
        try:
            id = int(input("ID >> "))
            new_password = input("Ingrese las nueva contraseña >> ")

            cursor = connection.cursor()
            cursor.execute("""
                        UPDATE public."Users"
	                        SET "Password"=%s
	                        WHERE "ID" = %s;
                           """, (new_password,id))
            print("GoFIles (LOG) >> Actualización exitosa!")
            return True
        except Exception as ex:
            print("GoFIles (ERROR) >> ", ex)
            return False
        

    panel = """
            || GoFiles Database Panel ||
                Opciones o comandos

              1.- Insertar un nuevo usuario
              2.- Eliminar un usuario
              3.- Actuilizar las credenciales de un usuario

              4.- Subir un archivo
              5.- Eliminar un archivo
              6.- Ver los archivos subidos
            """

    comando = ""

    while comando.upper() != "EXIT":
        print(panel)
        comando = input("GoFiles DB Admin >> ")
        
        if comando == "1":
            insertar_usuario()
            if insertar_usuario() == False:
                break


        if comando == "2":
            eliminar_usuario()
            if eliminar_usuario() == False:
                break
    
        if comando == "3":
            actualizar_usuario()
            if actualizar_usuario() == False:
                break



    

except Exception as ex:
    print(ex)

finally:
    connection.close()
    print("Conexión finalizada")