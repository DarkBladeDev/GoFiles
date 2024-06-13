import flet as ft
import time
from datetime import datetime #pip install DateTime
import psycopg2
from MODULES.db_control import get_creds 


def main(page: ft.Page):
    page.title = "GoFiles | Panel"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_login(e):
        page.remove(login_panel)
        page.add(carga)
        for i in range(0, 50):
            pr.value = i * 0.1
            time.sleep(0.1)
            page.update()
        page.remove(carga)
        page.add(
                main_menu,
                column_1,
                obtener_archivos()
                )
        page.overlay.append(pick_files_dialog)
        return True
        

    page.on_login = on_login
    
    on_login

    def connect_db():
        try:
            connection = psycopg2.connect(
                host=get_creds('HOST'),
                database=get_creds('DATABASE'),
                user=get_creds('USER'),
                password=get_creds('PASSWORD')
                )
            return connection

        except Exception as ex:
            print(ex)


    def close_banner(e):
        banner.open = False
        page.update()

    def account_info(e):
        banner.open = True
        page.update()

    def logout():
        page.remove(
            main_menu,
            column_1,
            obtener_archivos()
        )
        page.add(
                login_panel,
                error_no_account
                )
        
    
    def error_file():
        error_no_file_selected.open = True
        page.update()


    def open_file(e: ft.FilePickerResultEvent):
        file_path = str(e.files[0].path)

        print("LOG >> ", file_path)

        if file_path != "None":
            with open(file_path, 'rb') as f:
                file = f.read()
                file_name = f.name
                file_date_old = datetime.now().date()
                print("Archivo procesado!")
                file_date_new = file_date_old.strftime("%d/%m/%Y")

            connect_db()
            cursor = connect_db().cursor()
            cursor.execute("""
                           INSERT INTO public."Files"(
	                            filename, filedate, file)
	                            VALUES (%s, %s, %s);
                            """, (file_name, file_date_new, file))

            connect_db().commit()
            connect_db().close()
            msg_file_upload_comlete.open = True

        else:
            error_file()


    pick_files_dialog = ft.FilePicker(on_result=open_file)
    page.overlay.append(pick_files_dialog)

    
    


    # --------------- SNACKBARS ----------------- #
    
    error_no_account = ft.SnackBar(
        content= ft.Text(
            value= "Credenciales incorrectas o inexistentes",
            color= ft.colors.RED
                        )
    )

    error_no_file_selected = ft.SnackBar(
        content= ft.Text(
            value= "Debe seleccionar al menos un archivo",
            color= ft.colors.RED
                        )
    )

    msg_file_upload_comlete = ft.SnackBar(
        content= ft.Text(
            value= "Archivo subido exitosamente!!",
            color= ft.colors.GREEN
        )
    )
    # ---------------------------------------- #


    user = ft.TextField(
                label="Nombre de usuario"
            )

    password = ft.TextField(
                label="Contraseña",
                password=True,
                can_reveal_password=True
            )

    login_panel = ft.Column(
        controls=[
            ft.ElevatedButton(
                text='Iniciar sesión con GitHub',
                on_click=on_login,
                color= ft.colors.LIGHT_BLUE
            )
        ]
    )


    banner = ft.Banner(
        bgcolor= ft.colors.AMBER_100,
        leading= ft.Icon(ft.icons.PERSON, color= ft.colors.GREEN, size= 40),
        content= ft.Text(value="Nombre de usuario: " +  user.value, size=25),
        actions= [
            ft.TextButton("Cerrar", on_click= lambda _:close_banner),
        ],
    )


    column_1 = ft.Column()
    page.theme_mode = ft.ThemeMode.LIGHT
    appbar_text_ref = ft.Ref[ft.Text]()
    page.title = "GoFiles"
    

    page.appbar = ft.AppBar(
        title=ft.Text("GoFiles", ref=appbar_text_ref),
        center_title=True,
        bgcolor=ft.colors.BLUE
    )


    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.GREY_300,
            mouse_cursor={ft.MaterialState.HOVERED: ft.MouseCursor.WAIT,
                          ft.MaterialState.DEFAULT: ft.MouseCursor.ZOOM_OUT},
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Archivo"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Abrir"),
                        leading=ft.Icon(ft.icons.FILE_OPEN),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=lambda _: pick_files_dialog.pick_files()
                    )
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Cuenta"),
                controls=[
                    ft.MenuItemButton(
                        content= ft.Text("Mis datos"),
                        leading= ft.Icon(ft.icons.PERSON),
                        style= ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click= lambda _:account_info
                    ),
                    ft.MenuItemButton(
                        content= ft.Text("Cerrar sesión"),
                        leading= ft.Icon(ft.icons.LOGOUT),
                        style= ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED_100}),
                        on_click= lambda _:logout()
                    )
                ]
            )
        ]
    )

    file_listview = ft.ListView(
        expand=True
    )
    upload_button = ft.ElevatedButton(text="Subir", on_click=pick_files_dialog.pick_files)

    main_menu = ft.Row([menubar])

    pr = ft.ProgressRing(
                color= ft.colors.BLUE,
                width= 50,
                height= 50,
                stroke_width = 2
            )

    carga = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand= True,
        controls= [
            pr
        ]
    )


    # Realizar la consulta SQL para obtener los archivos de la base de datos
    def obtener_archivos():
        connect_db()

        cursor = connect_db().cursor()
        cursor.execute("""
                    SELECT * FROM public."Files";
                    """)
        archivos = cursor.fetchall()
        connect_db().close()

        # Crear una lista vacía para almacenar las filas de la tabla de datos
        rows = []

        # Iterar a través de los archivos y agregar una nueva fila a la lista para cada archivo
        for archivo in archivos:
            file_id, file_name, file_date = archivo
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(file_id)),
                    ft.DataCell(ft.Text(file_name)),
                    ft.DataCell(ft.Text(file_date))
                ]
            )
            rows.append(row)

        # Establecer la lista de filas en la tabla de datos
        data_table = ft.DataTable(
            show_checkbox_column= True,
            bgcolor=ft.colors.GREY_100,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre del archivo")),
                ft.DataColumn(ft.Text("Fecha de modificación"))
            ],
            rows=rows
        )

        return data_table

    column_1.controls.append(file_listview)
    column_1.controls.append(upload_button)

    page.add(
        login_panel,
        error_no_account
        )
    
ft.app(target= main,
        name= "GoFiles",
        port=8000,
        view=ft.WEB_BROWSER)
