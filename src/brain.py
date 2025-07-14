#literally, the brain# main.py

import os, json,argparse, google.generativeai as genai
from dotenv import load_dotenv
from src.load_chat import choose_chat
from src.utils.cli import get_user_input
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()
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
        # importing chat history to the terminal
        if self.history:
            for message in self.history:
                role = message["role"]
                content = "\n".join(message["parts"]).strip()

                if role == "user":
                    self.console.print(f"[bold magenta]You:[/] {content}")
                elif role == "model":
                    self.console.print(f"[bold green]Nomi: [/]", end="")
                    self.console.print(Markdown(content))
                self.console.print("")
        
        # Greeting the user
        try:
            console.print("[bold cyan]\n\n\nL O A D I N G . . . \n\n\n[/bold cyan]")
            greeter = genai.GenerativeModel(self.model_name, system_instruction=self.persona)
            greeting = greeter.generate_content("Greet the user warmly as Nomi.")
            welcome_text = Markdown(greeting.text.strip())
            self.console.print("[bold cyan]Nomi: [/]", end="")
            self.console.print(welcome_text)
            self.console.print("")
        except Exception as e:
            self.console.print("[bold cyan]Nomi is ready. Ask me anything![/bold cyan]")

        """
        Chat loop which I'm sending to nomi.py
        """

        while True:
            console.print("[bold magenta]You:[/bold magenta] ", end="")
            user_input= get_user_input()
            if user_input.lower() in ["exit", "quit", "bye"]:
                self.console.print("")
                self.console.print("[italic dim]Goodbye, human. See you later :)[/italic dim]")
                break
            
            self.console.print("")
            response = self.generate_response(user_input)
            md_response = Markdown(response)
            self.console.print(f"[bold green]Nomi: [/]", end="")
            self.console.print(md_response)
            self.console.print("")

        self.console.print("\n[dim]Press Enter to exit...[/dim]")
        input()