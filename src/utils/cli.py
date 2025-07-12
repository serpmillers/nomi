#cli 
from rich.prompt import Prompt

def get_user_input():
    return Prompt.ask("[bold magenta]You[/bold magenta]")
