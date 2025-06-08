import flet as ft
from data import clientes, produtos, vendas


def gerar_relatorios():
    vendas_por_cliente = {}
    vendas_por_produto = {}
    total_geral = 0

    for venda in vendas:
        cliente = venda["cliente"]
        vendas_por_cliente[cliente] = vendas_por_cliente.get(cliente, 0) + 1
        total_geral += venda["valor_total"]

        for produto in venda["produtos"]:
            nome = produto["nome"]
            vendas_por_produto[nome] = vendas_por_produto.get(nome, 0) + 1

    return vendas_por_cliente, vendas_por_produto, total_geral


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def criar_card(titulo, valor, icone, cor_icon, cor_fundo):
    return ft.Container(
        content=ft.Row([
            ft.Icon(icone, size=40, color=cor_icon),
            ft.Column([
                ft.Text(titulo, size=14, weight="w500", color=ft.Colors.GREY_800),
                ft.Text(valor, size=22, weight="bold", color=cor_icon),
            ], spacing=2)
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15,
        bgcolor=cor_fundo,
        border_radius=15,
        expand=True,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
    )


def criar_tabela(titulo, dados, col1, col2):
    return ft.Column([
        ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
        ft.Container(
            content=ft.Text("Nenhuma venda registrada.") if not dados else ft.DataTable(
                heading_row_color=ft.Colors.GREY_100,
                columns=[
                    ft.DataColumn(label=ft.Text(col1, weight="bold")),
                    ft.DataColumn(label=ft.Text(col2, weight="bold")),
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(k))),
                        ft.DataCell(ft.Text(str(v))),
                    ])
                    for k, v in dados.items()
                ]
            ),
            padding=10,
            bgcolor=ft.Colors.GREY_50,
            border_radius=10
        ),
        ft.Divider()
    ], spacing=10)


def View(page: ft.Page):
    def VaiPraHome(e):
        page.go("/home")

    vendas_por_cliente, vendas_por_produto, total_geral = gerar_relatorios()

    cards = ft.Row([
        criar_card("Total de Vendas", formatar_moeda(total_geral), ft.Icons.ATTACH_MONEY,
                   ft.Colors.GREEN_500, ft.Colors.GREEN_50),
        criar_card("Produtos", str(len(produtos)), ft.Icons.INVENTORY_2,
                   ft.Colors.BLUE_500, ft.Colors.BLUE_50),
        criar_card("Clientes", str(len(clientes)), ft.Icons.PEOPLE,
                   ft.Colors.ORANGE_500, ft.Colors.ORANGE_50),
    ], spacing=15)

    return ft.View(
        route="/relatorios",
        appbar=ft.AppBar(
            title=ft.Row([
                ft.Icon(name=ft.Icons.ASSESSMENT_ROUNDED, color=ft.Colors.WHITE),
                ft.Text("Relatórios", color=ft.Colors.WHITE),
            ], spacing=10),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=VaiPraHome),
            bgcolor=ft.Colors.YELLOW_500
        ),
        controls=[
            ft.Container(cards, padding=20),
            ft.Container(
                content=ft.Column([
                    criar_tabela("📊 Vendas por Cliente", vendas_por_cliente, "Cliente", "Qtd. de Vendas"),
                    criar_tabela("📦 Vendas por Produto", vendas_por_produto, "Produto", "Qtd. Vendida"),
                    ft.Text(
                        f"💰 Total Geral de Vendas: {formatar_moeda(total_geral)}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700
                    )
                ], spacing=20),
                padding=20
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
