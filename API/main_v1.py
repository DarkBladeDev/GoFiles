from fastapi import FastAPI, status, HTTPException, Request
import requests
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import flet as ft
import urllib.parse
import json
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional


app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="./API/static"), name="static")
templates = Jinja2Templates(directory="./API/templates")

API_HOST = '127.0.0.1'
DATABASE_URL = "postgresql+psycopg2://gofiles:antuan1357@localhost/GoFiles"


app.add_middleware(HTTPSRedirectMiddleware)

# OAuth2 settings
oauth2_scheme = OAuth2(
    flows={
        "authorizationCode": {
            "authorizationUrl": "https://github.com/login/oauth/authorize",
            "tokenUrl": "https://github.com/login/oauth/access_token",
        }
    },
    scheme_name="OAuth2",
)


engine = create_engine(DATABASE_URL)
def get_creds(credential_name: str):
    """
    Obtiene credenciales mediante ésta función

    Args:
    - credential_name (str): Nombre exacto del credencial a utilizar.

    Returns:
    - result: Resultado de la consulta de crendenciales
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    session.execute("""
                    SELECT %s
                        FROM public."Credentials";
                    """, (credential_name))
    result = session.get_transaction()

    session.close()

    return result



async def github_authenticate_user(access_token: str) -> dict:
    """
    Autenticar usuario utilizando el token de acceso

    Args:
    - access_token (str): Token de acceso obtenido después de la autorización

    Returns:
    - dict: Información del usuario autenticado
    """
    # Configuración de la API de autenticación
    auth_api_url = "https://api.github.com/user"
    auth_api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Realizar solicitud HTTP GET a la API de autenticación
        response = requests.get(auth_api_url, headers=auth_api_headers)

        # Verificar si la respuesta es exitosa (200 OK)
        if response.status_code == 200:
            user_response = response.json()
            user_info = {
                "id": user_response["id"],
                "username": user_response["username"],
                "email": user_response["email"]
            }
            return user_info
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error al autenticar al usuario")
    except Exception as e:
        # Manejar errores de conexión o solicitud
        raise Exception(f"Error autenticando usuario: {e}")

async def github_get_token(code: str):
    client_id = get_creds('CLIENT_ID')
    client_secret = get_creds('CLIENT_SECRET')
    redirect_uri = f"https://{API_HOST}:8550/oauth_callback"

    token_url = "https://github.com/login/oauth/access_token"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    # Realizar la solicitud de token
    response = requests.post(token_url, headers=headers, data=data)

    # Procesar la respuesta
    if response.status_code == 200:
        print(response.text)
        token_response = response.json()
        access_token = token_response["access_token"]
        # Ahora puedes utilizar el token de acceso para autenticar al usuario
        return access_token
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al obtener el token de acceso")



@app.get("/github/oauth_callback")
async def github_oauth_callback(code: str, state: str):
    # Intercambiar el código de autorización por un token de acceso
    access_token = await github_get_token(code)

    # Autenticar al usuario utilizando el token de acceso
    user_info = await github_authenticate_user(access_token)
    # Enviar la información del usuario a la aplicación Flet
    user_info_json = json.dumps(user_info)
    user_info_encoded = urllib.parse.quote(user_info_json)
    return RedirectResponse(url=f"https://{API_HOST}:8550/flet_app?user_info={user_info_encoded}", status_code=302)



@app.get("/google/oauth_callback")
async def google_oauth_callback(code: str):
    # Crea un objeto de flujo de autenticación de Google
    flow = Flow.from_client_secrets_file(
        client_secrets_file='env/creds/client_secret.json',
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"],
        redirect_uri= f"https://{API_HOST}:8550/google/oauth_callback"
    )

    # Utiliza el código de autorización para obtener un token de acceso de Google
    flow.fetch_token(code=code)

    # Crea un objeto de credenciales de Google
    credentials = Credentials.from_authorized_user_info(flow.credentials.to_json())

    # Redirige al usuario a la página principal de la aplicación
    # Enviar la información del usuario a la aplicación Flet
    user_info_json = json.dumps(credentials)
    user_info_encoded = urllib.parse.quote(user_info_json)
    return RedirectResponse(url=f"/flet_app?user_info={user_info_encoded}", status_code=302)



@app.get("/github")
async def github_login_panel():
    from APP.Github_login import login
    import nest_asyncio
    
    nest_asyncio.apply()
    github_login_app =  ft.app(target=login,
                        view=ft.WEB_BROWSER
                        )

    return github_login_app


@app.get("/google")
async def google_login_panel():
    from APP.Google_login import login
    import nest_asyncio
    
    nest_asyncio.apply()
    google_login_app =  ft.app(target=login,
                        view=ft.WEB_BROWSER
                        )

    return google_login_app



# Flet app endpoint
@app.get("/flet_app")
async def flet_app(user_info: str):
    # Create a new Flet app instance
    from APP.GoFiles_V1 import main
    import nest_asyncio
    
    nest_asyncio.apply()

    gofiles = ft.app(target=main,
                 view=ft.WEB_BROWSER)
    # Pass the user info to the Flet app
    gofiles.user_info = user_info

    # Return the Flet app
    return gofiles



def selctor(page: ft.Page):

    # PROPIEDADES DE LA PÁGINA ------------------------------------------
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "GoFiles"
    # -------------------------------------------------------------------

    github_button = ft.ElevatedButton(
        text= "Iniciar sesion con GitHub.",
        color=ft.colors.BLUE,
        on_click= lambda _: github()
    )

    google_button = ft.ElevatedButton(
        text= "Iniciar sesion con Google.",
        color=ft.colors.GREEN,
        on_click= lambda _: google()
        )
    

    page.add(github_button,
            google_button)


def event_handler(redirect: Optional(str) = None):
    global event
    event = True
    if redirect != None:
        return RedirectResponse(url=f"{redirect}", status_code=302)

    
def github():
    event_handler("/github/oauth_callback")
    return True
    
def google():
    event_handler("/google/oauth_callback")
    return True



@app.get("/")
async def root():
    import nest_asyncio
    nest_asyncio.apply()


    auth_selector = ft.app(target=selctor, view=ft.AppView.WEB_BROWSER)
    while event_handler() != RedirectResponse:
        if github == True:
            return RedirectResponse(url="/github/oauth_callback", status_code=302)
        elif google == True:
            return RedirectResponse(url="/google/oauth_callback", status_code=302)
    
    return auth_selector


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=8550, ssl_certfile='./certs/cert.pem', ssl_keyfile='./certs/key.pem')


