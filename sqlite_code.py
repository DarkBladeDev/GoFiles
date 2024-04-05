import sqlite3
import os


con = sqlite3.connect('GoFiles.db')
cursor = con.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT
)""")


class User:
    def verificar_credenciales(usuario, contraseña):
        conn = sqlite3.connect('GoFiles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USUARIOS WHERE username = ? AND password = ?", (usuario, contraseña))
        
        resultados = cursor.fetchall()
        
        conn.close()
        
        if resultados != []:
            print("Iniciando sesion...")
            return True
        elif resultados == []:
            print("Credenciales incorrectas.")
            return False



def registrar(username, password):
    con = sqlite3.connect('GoFiles.db')
    cursor = con.cursor()
    cursor.execute(f"INSERT INTO usuarios VALUES (?, ?)", (username, password))
    con.commit()
    con.close()

def select():
    con = sqlite3.connect('GoFiles.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    print(usuarios)
    con.close()

def deleteRow(username, password):
    conn = sqlite3.connect("GoFiles.db")
    cursor = conn.cursor() 
    instruccion_1 = f"DELETE FROM usuarios WHERE username like '{username}'"
    instruccion_2 = f"DELETE FROM usuarios WHERE username like '{password}'"
    cursor.execute(instruccion_1)
    cursor.execute(instruccion_2)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    os.system("cls")

    comando = 1
    while comando != "Exit" or comando != "exit":
        comando = input("GoFiles: Admin >> ")
        if comando == "Register" or comando == "register":
            arg_1 = input("Username >> ")
            arg_2 = input("Password >> ")
            registrar(arg_1, arg_2)

        if comando == "Delete" or comando == "delete":
            arg_1 = input("Username >> ")
            arg_2 = input("Password >> ")
            deleteRow(arg_1, arg_2)

        if comando == "Show" or comando == "show":
            select()

        if comando == "Exit" or comando == "exit":
            break