import flet as ft
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage

load_dotenv()


def initialize_langchain():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)
    return model, logger


def agent_executor(input_data, model, logger):
    question, chat_history = input_data["question"], input_data["chat_history"]
    try:
        messages = []
        for user_msg, bot_msg in chat_history:
            messages.append(HumanMessage(content=user_msg))
            messages.append(AIMessage(content=bot_msg))
        messages.append(HumanMessage(content=question))

        response = model.invoke([HumanMessage(content=messages)])
        return response.content
    except Exception as e:
        logger.error(f"Erro ao processar: {e}")
        return "Ocorreu um erro. Por favor, tente novamente mais tarde."


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message):
        super().__init__()

        self.alignment = "start"
        self.spacing = 5

        avatar = ft.CircleAvatar(
            content=ft.Text(
                self.get_initials(message.user_name), color=ft.Colors.WHITE
            ),
            bgcolor=self.get_avatar_color(message.user_name),
        )

        user_name_text = ft.Text(message.user_name, weight="bold")
        message_text = ft.Text(message.text, selectable=True, width=900)

        message_column = ft.Column(
            controls=[user_name_text, message_text], tight=True, spacing=5
        )

        self.controls = [avatar, message_column]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize() if user_name else "U"

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
    model, logger = initialize_langchain()
    chat_history = []

    user_name = "User"
    max_history = 5

    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    def display_message(name, text):
        msg = Message(name, text, "chat_message")
        chat.controls.append(ChatMessage(msg))

    def send_message_click(e):
        user_input = new_message.value.strip()
        if user_input:
            display_message(user_name, user_input)

            response = agent_executor(
                {"question": user_input, "chat_history": chat_history},
                model,
                logger,
            )

            display_message("Agent", response)
            chat_history.append((user_input, response))
            if len(chat_history) > max_history:
                chat_history.pop(0)

            new_message.value = ""
            page.update()

    new_message = ft.TextField(
        hint_text="Escreva uma mensagem...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=None,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED, tooltip="Enviar mensagem", on_click=send_message_click
    )

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [new_message, send_button],
            alignment="end",
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)
