#literally, the brain# main.py

import os, json, google.generativeai as genai
from dotenv import load_dotenv
from src.load_chat import choose_chat
from src.utils.cli import get_user_input
from rich.console import Console

load_dotenv()

class Brain:
    def __init__(self, config):
        """
        Data from config and .env so that the bot can work
        """
        self.console = Console()
        self.config = config
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.persona = config.get("persona", "")
        self.model_name = config.get("default_model", "gemini-1.5-flash-002")

        if not self.api_key:
            self.console.print("[bold red]Error:[/] GEMINI_API_KEY not found in .env file.")
            exit(1)

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            self.model_name,
            system_instruction=self.persona
        )
        self.chat_name, self.history = choose_chat()
        self.chat_path = os.path.join("chats", self.chat_name + ".json")
        self.chat_session = self.model.start_chat(
            history=self.history
        )

    def generate_response(self, user_input: str) -> str:
        try:
            response = self.chat_session.send_message(user_input)

            # updating history on the go
            self.history.append({
                "role": "user",
                "parts": [user_input]
            })
            self.history.append({
                "role": "model",
                "parts": [response.text.strip()]
            })

            # saving chat history to file
            with open(self.chat_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
            
            return response.text.strip()
        
        except Exception as e:
            return f"[Error] Something went wrong: {e}"

    def chat(self):
        self.console.print("[bold cyan]Nomi is ready. Ask me anything![/bold cyan]")

        """
        Chat loop which I'm sending to nomi.py
        """

        while True:
            user_input= get_user_input()
            if user_input.lower() in ["exit", "quit", "bye"]:
                self.console.print("[italic dim]Goodbye, human. See you later :)[/italic dim]")
                break

            response = self.generate_response(user_input)
            self.console.print(f"[bold green]Nomi:[/] {response}")

        self.console.print("\n[dim]Press Enter to exit...[/dim]")
        input()