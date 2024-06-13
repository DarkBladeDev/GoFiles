import flet as ft
from google_auth_oauthlib.flow import Flow

def login(page: ft.Page):
    page.title = "GoFiles | Google Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #google_login_button = ft.ElevatedButton(text="Iniciar sesión con Google", on_click=lambda _: handle_google_login(page))

    #def handle_google_login(page: ft.Page):
        # Crea un objeto de flujo de autenticación de Google
    flow = Flow.from_client_secrets_file(
        "env/creds/client_secret.json",
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"],
        redirect_uri="https://192.168.0.11:8550/google/oauth_callback"
    )

        # Obtiene la URL de inicio de sesión de Google
    authorization_url, _ = flow.authorization_url(prompt="consent")

        # Redirige al usuario a la página de inicio de sesión de Google
    page.launch_url(authorization_url)

    #page.add(google_login_button)


#ft.app(target=login)