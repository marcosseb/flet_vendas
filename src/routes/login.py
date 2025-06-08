import flet as ft
from data import usuarios  # Lista com dicionários: nome, email, empresa, usuario, senha

def View(page: ft.Page):
    mensagem_erro = ft.Text(
        value="",
        color=ft.Colors.RED_700,
        visible=False,
        size=14,
        weight=ft.FontWeight.BOLD
    )

    def VaiPraHome(e):
        usuario = txtLogin.value.strip()
        senha = txtSenha.value.strip()

        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                mensagem_erro.visible = False
                mensagem_erro.value = ""

                # Armazena o nome de usuário no client_storage
                page.client_storage.set("usuario_logado", u["usuario"])

                page.go("/home")
                return

        mensagem_erro.visible = True
        mensagem_erro.value = "Usuário ou senha incorretos!"
        page.update()

    def VaiPraCadastro(e):
        page.go("/cadastro_login")

    logo = ft.Image(
        src="seven.png",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN
    )

    txtLogin = ft.TextField(
        label="Usuário",
        prefix_icon=ft.Icons.PERSON,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_100,
    )

    txtSenha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_100,
    )

    btnEntrar = ft.ElevatedButton(
        text="ENTRAR",
        on_click=VaiPraHome,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.INDIGO_700,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=40, vertical=15),
            shape=ft.RoundedRectangleBorder(radius=12),
        )
    )

    row_buttons = ft.TextButton(
        "Não tem uma conta? Cadastre-se",
        on_click=VaiPraCadastro
    )

    card_login = ft.Container(
        content=ft.Column(
            [
                logo,
                ft.Text("SEVEN SYSTEM", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
                ft.Text("Acesse sua conta", size=16, color=ft.Colors.GREY_600),
                txtLogin,
                txtSenha,
                mensagem_erro,
                btnEntrar,
                row_buttons,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=30,
        width=360,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLUE_GREY_100, spread_radius=0.5),
    )

    return ft.View(
        route="/login",
        controls=[
            ft.Container(
                content=card_login,
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.Colors.BLUE_GREY_50
            )
        ]
    )
