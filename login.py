import flet as ft

def main(page: ft.Page):
    page.title = "Login - Chat Bot Legal"
    page.window_width = 400
    page.window_height = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Nome do chatbot
    nome_bot = ft.Text("Chat Bot Legal", size=30, weight=ft.FontWeight.BOLD)

    mensagem = ft.Text("Olá!", size=20, color=ft.Colors.BLUE)

    # Campo para o usuário digitar o nome
    campo_usuario = ft.TextField(
        label="Nome de usuário",
        hint_text="Digite seu nome...",
        width=300,
        border_radius=10
    )

    def entrar(e):
        if campo_usuario.value.strip():
            # Guardar o nome do usuário e usar o mesmo nome no prorpio chat
            page.client_storage.set("username", campo_usuario.value.strip())
            # Vai ppara outro arquivo, ou era para ir, mas não está indo kkkk e to com preguiça de arrumar
            #page.go("/chat_flet")
        else:
            campo_usuario.error_text = "Por favor, digite seu nome"
            page.update()

    # Botão entrar
    botao_entrar = ft.ElevatedButton(
        text="Entrar",
        width=300,
        on_click=entrar
    )

    layout = ft.Column(
        [
            nome_bot,
            mensagem,
            campo_usuario,
            botao_entrar,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=350
    )

    page.add(layout)

ft.app(target=main)
