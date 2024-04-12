import flet as ft
import sqlite3 as sql
import time


def main(page: ft.Page):

    class User:
        def verificar_credenciales(usuario, contraseña):
            conn = sql.connect('GoFiles.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USUARIOS WHERE username = ? AND password = ?", (usuario, contraseña))
            
            resultados = cursor.fetchall()
            
            conn.close()
            
            if resultados != []:
                page.remove(login_panel)
                page.add(carga)
                time.sleep(3)
                page.remove(carga)
                page.add(
                    main_menu,
                    column_1
                )
                return True
            elif resultados == []:
                error_no_account.open = True
                page.update()
                return False


    def close_banner(e):
        banner.open = False
        page.update()

    def account_info(e):
        banner.open = True
        page.update()

    def logout():
        page.remove(
            main_menu,
            column_1
        )
        page.add(login_panel)
    
    def error_file():
        error_no_file_selected.open = True
        page.update()


    def open_file(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else error_file()
        )
        selected_files.update()

    selected_files = ft.Text()
    pick_files_dialog = ft.FilePicker(on_result=open_file)
    page.overlay.append(pick_files_dialog)


    # --------------- ERRORES ----------------- #
    
    error_no_account = ft.SnackBar(
        content= ft.Text(value= "Credenciales incorrectas o inexistentes"
                        )
    )

    error_no_file_selected = ft.SnackBar(
        content= ft.Text(
            value= "Debe seleccionar al menos un archivo"
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
            user,
            password,
            ft.ElevatedButton(
                text='Iniciar sesión',
                on_click=lambda _:User.verificar_credenciales(user.value, password.value)
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
                        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True)
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

    upload_button = ft.ElevatedButton(text="Subir", on_click=open_file)

    main_menu = ft.Row([menubar])

    carga = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand= True,
        controls= [
            ft.ProgressBar(width=1400,
                            color="amber",
                            bgcolor="#eeeeee"
                            )
        ]
    )



    column_1.controls.append(file_listview)
    column_1.controls.append(upload_button)

    page.add(
        login_panel,
        error_no_account
        )





ft.app(target= main,
        assets_dir= 'assets',
        name= "GoFiles")
