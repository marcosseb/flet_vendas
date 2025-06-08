import flet as ft
from data import usuarios

def View(page: ft.Page):
    usuario_logado = page.client_storage.get("usuario_logado")
    dados_usuario = next((u for u in usuarios if u["usuario"] == usuario_logado), None)

    if not dados_usuario:
        page.go("/login")
        return

    nome_empresa_text = ft.Text(f"{dados_usuario['empresa']}", size=20, weight="bold")

    def abrir_edicao_empresa(e):
        nome_empresa_input = ft.TextField(label="Nome da Empresa", value=dados_usuario["empresa"], width=400)

        def salvar_nome_empresa(ev):
            dados_usuario["empresa"] = nome_empresa_input.value
            nome_empresa_text.value = nome_empresa_input.value
            page.client_storage.set("empresa", nome_empresa_input.value)

            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text("Nome da empresa atualizado!"), bgcolor=ft.colors.GREEN)
            page.snack_bar.open = True
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Nome da Empresa"),
            content=nome_empresa_input,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(dialog)),
                ft.TextButton("Salvar", on_click=salvar_nome_empresa),
            ],
            actions_alignment="end"
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def abrir_dialogo_alterar_senha(e):
        senha_atual = ft.TextField(label="Senha Atual", password=True, can_reveal_password=True)
        nova_senha = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True)
        confirmar_senha = ft.TextField(label="Confirmar Nova Senha", password=True, can_reveal_password=True)
        mensagem_feedback = ft.Text("", color=ft.colors.RED, size=12, opacity=0)

        def senha_forte(s):
            return (
                len(s) >= 8 and
                any(c.islower() for c in s) and
                any(c.isupper() for c in s) and
                any(c.isdigit() for c in s) and
                any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in s)
            )

        def mostrar_mensagem(texto, cor):
            mensagem_feedback.value = texto
            mensagem_feedback.color = cor
            mensagem_feedback.opacity = 1
            page.update()

        def limpar_mensagem():
            mensagem_feedback.opacity = 0
            page.update()

        def confirmar_alteracao(ev):
            if senha_atual.value != dados_usuario["senha"]:
                mostrar_mensagem("Senha atual incorreta!", ft.colors.RED)
            elif nova_senha.value != confirmar_senha.value:
                mostrar_mensagem("As senhas novas não coincidem!", ft.colors.RED)
            elif nova_senha.value == dados_usuario["senha"]:
                mostrar_mensagem("A nova senha não pode ser igual à anterior!", ft.colors.RED)
            elif not senha_forte(nova_senha.value):
                mostrar_mensagem("A nova senha não é forte o suficiente!", ft.colors.RED)
            else:
                dados_usuario["senha"] = nova_senha.value
                senha_atual.value = nova_senha.value = confirmar_senha.value = ""
                mostrar_mensagem("Senha alterada com sucesso!", ft.colors.GREEN)

                dialog.open = False  # Correção 2 aplicada: fecha o diálogo
                page.update()

                page.run_task(lambda: esconder_mensagem_depois())

        async def esconder_mensagem_depois():
            await page.sleep(2)
            limpar_mensagem()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Alterar Senha"),
            content=ft.Column(
                [senha_atual, nova_senha, confirmar_senha, mensagem_feedback],
                tight=True
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(dialog)),
                ft.TextButton("Salvar", on_click=confirmar_alteracao),
            ],
            actions_alignment="end"
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def fechar_dialogo(dialog):
        dialog.open = False
        page.update()

    return ft.View(
        route="/configuracoes",
        appbar=ft.AppBar(
            title=ft.Text("Configurações", color=ft.colors.WHITE),
            bgcolor=ft.colors.GREEN_900,
            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.WHITE, on_click=lambda e: page.go("/home"))
        ),
        controls=[
            ft.Column([
                ft.Row([
                    nome_empresa_text,
                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar Nome da Empresa", on_click=abrir_edicao_empresa)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=500),
                ft.Divider(),
                ft.Text("Preferências", style="titleMedium"),
                ft.Switch(label="Receber notificações", value=True),
                ft.Divider(),
                ft.ElevatedButton("Alterar Senha", icon=ft.icons.LOCK, on_click=abrir_dialogo_alterar_senha),
                ft.Divider(),
                ft.Text("Sobre o App", style="titleMedium"),
                ft.Text("Versão: 1.0.0"),
                ft.Text("Desenvolvido por: Você"),
                ft.Text("© 2025 - Todos os direitos reservados"),
            ],
            spacing=20,
            width=500
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
