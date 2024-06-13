import flet as ft


def selctor(page: ft.Page):

    # PROPIEDADES DE LA PÁGINA ------------------------------------------
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "GoFiles"
    # -------------------------------------------------------------------

    github_button = ft.ElevatedButton(
        text= "Iniciar sesion con GitHub.",
        color=ft.colors.BLUE,
        on_click= lambda _: github(True)
    )

    google_button = ft.ElevatedButton(
        text= "Iniciar sesion con Google.",
        color=ft.colors.GREEN,
        on_click= lambda _: google(True)
        )
    

    page.add(github_button,
            google_button)

github_auth = False
google_auth = False
    
def github(authenticated):
    global github_auth
    github_auth = authenticated
    
def google(authenticated):
    global google_auth
    google_auth = authenticated