#literally, the brain# main.py

import os, google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
# from src.memory import Memory

load_dotenv()

class Brain:
    def __init__(self, config):
        self.console = Console()
        self.config = config
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.persona = config.get("persona", "")
        self.model_name = config.get("default_model", "gemini-1.5-flash-002")

        if not self.api_key:
            self.console.print("[bold red]Error:[/] GEMINI_API_KEY not found in .env file.")
            exit(1)

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate_response(self, user_input: str) -> str:
        try:
            prompt = f"{self.persona}\nUser: {user_input}\nNomi: "
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"[Error] Something went wrong: {e}"
