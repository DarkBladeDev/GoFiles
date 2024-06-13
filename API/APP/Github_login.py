import flet as ft
from API.MODULES.db_control import get_creds
from flet.auth.providers import GitHubOAuthProvider

def login(page: ft.Page):
    page.title = "GoFiles | GitHub Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    github_provider = GitHubOAuthProvider(
        client_id = get_creds('CLIENT_ID'),
        client_secret = get_creds('CLIENT_SECRET'),
        redirect_url= ""
        )
    page.login(github_provider)

#ft.app(target=login, view=ft.AppView.WEB_BROWSER)