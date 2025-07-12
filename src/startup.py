#fancy intro type shi

import yaml, os
from contextlib import contextmanager
from rich.prompt import Prompt, Confirm
from rich.console import Console

console = Console()

class Startup:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.models = {
            "gemini-1.5-flash": "Fast & efficient",
            "gemini-1.5-pro": "Better reasoning",
            "gemini-2.5-flash": "Mid-2025 speedster",
            "gemini-2.5-pro": "Strongest (might be overkill)"
        }

    def is_first_run(self):
        return not os.path.exists(self.config_path)
    
    @contextmanager
    def alternate_screen(self):
        """Context manager to use alternate screen buffer."""
        os.system("tput smcup")
        os.system("clear")
        try:
            yield
        finally:
            os.system("clear")
            os.system("tput rmcup")

    def get_saved_model(self):
        if not os.path.exists(self.config_path):
            return None
        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f)
        return data.get("default_model")
    
    def save_model(self,model_name):
        config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f) or {}
        config["default_model"] = model_name 
        with open(self.config_path, "w") as f:
            yaml.dump(config, f)
    
    def choose_model(self):
        console.print("\n[bold green]Choose your default gemini model:[/bold green]")
        for i, (key, desc) in enumerate(self.models.items(), 1):
            console.print(f"[cyan]{i}.[/cyan] {key} - {desc}")

        index = Prompt.ask("\nEnter number", choices=[str(i) for i in range(1, len(self.models)+1)])
        model = list(self.models.keys())[int(index)-1]
        self.save_model(model)
        console.print(f"\nDefault model set to: [bold yellow]{model}[/bold yellow]\n")

    def run(self):
        if self.is_first_run():
            console.print("[bold]Welcome to Nomi![/bold]")
            self.choose_model()
        else:
            current_model = self.get_saved_model()
            console.print(f"Current model: [bold]{current_model}[/bold]")
            if Confirm.ask("Do you want to change it?"):
                self.choose_model()
        console.print("[bold cyan]Nomi is ready. Ask me anything![/bold cyan]")