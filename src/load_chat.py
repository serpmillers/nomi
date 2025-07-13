import os, json
from rich.console import Console
from rich.prompt import Prompt

console = Console()
chat_dir = "chats"
os.makedirs(chat_dir, exist_ok=True)

def list_chat_logs():
    """
    List all chats to choose from
    """
    return [
        f[:-5] # to remove extension from the name
        for f in os.listdir(chat_dir)
        if f.endswith(".json")
    ]

def choose_chat():
    chats = list_chat_logs()
    if not chats:
        console.print("[bold yellow]No chats found, lets create a new one! [/]")
        chat_name = Prompt.ask("Give it a name")
        history = []
        return chat_name, history
    
    console.print("[bold green]Your saved chats:[/]")
    for i, name in enumerate(chats, 1):
        console.print(f"[cyan]{i}.[/] {name}")
    console.print(f"[cyan]{len(chats)+1}[/] Create new chat: ")
    
    idx = Prompt.ask(
        "Enter number: ",
        choices=[str(i) for i in range(1, len(chats)+2)]
    )
    # if creating new chat
    if int(idx) == len(chats) + 1:
        chat_name = Prompt.ask("Give it a name: ")
        history = []
        return chat_name, history

    # if selecting existing chat
    chat_name = chats[int(idx) - 1]
    path = os.path.join(chat_dir, chat_name + ".json")
    with open(path, "r", encoding="utf-8") as f:
        history = json.load(f) or []

    console.print(f"\nLoaded chat: [bold]{chat_name}[/]\n")
    return chat_name, history