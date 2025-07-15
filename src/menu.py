#loading menu trial

import os, yaml, questionary, subprocess, platform
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

CONFIG_PATH = "config.yaml"
MODELS = {
    "gemini-1.5-flash": "Fast & efficient",
    "gemini-1.5-pro": "Better reasoning",
    "gemini-2.5-flash": "Mid-2025 speedster",
    "gemini-2.5-pro": "Strongest (might be overkill)"
}

console = Console()
chat_dir = "chats"

def center(text):
    return Align.center(Panel(text, expand=False))

def edit_config(model=None, persona=None):
    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)
    if model: cfg["default_model"] = model
    if persona is not None: cfg["persona"] = persona
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f)

def choose_model():
    model = questionary.select(
        "Pick a Gemini model:",
        choices = [f"{m} - {desc}" for m, desc in MODELS.items()
        ],
        qmark=" ❯ "
    ).ask()
    return model.split(" ")[0]

def edit_persona():
    with open(CONFIG_PATH, "r") as f:
        persona = yaml.safe_load(f).get("persona", "")
    new_p = questionary.text(
        "Edit your persona (leave blank if don't want to change):",
        default=persona
    ).ask()
    return new_p if new_p.strip() != "" else None

def choose_chat():
    from src.load_chat import choose_chat as load
    chat_name, _ = load()
    return chat_name

def delete_chat():
    chats = [
        f[:-5] # to remove extension from the name
        for f in os.listdir(chat_dir)
        if f.endswith(".json")
    ]
    choices = chats + ["Back"]
    selected = questionary.select(
        "Chat to delete: ",
        choices=choices,
        qmark=" ❯ "
    ).ask()
    if selected == "Back":
        return None
    
    chat_name = selected
    
    confirm = questionary.text(
        f"Are you sure you want to delete '{chat_name}'?\n  (Type 'yes' for confirming or 'no' for cancelling\n  ",
        qmark=" ❯ "
    ).ask()

    if confirm and confirm.strip().lower() == "yes":
        try:
            return chat_name
        except Exception as e:
            console.print(f"[red]Error:[/] {e}")

def launch_chat_window(chat_name):
    cmd = ["python3", "-m", "src.brain", chat_name]
    subprocess.Popen([
        "gnome-terminal",
        "--title",
        f"Nomi – {chat_name}",
        "--"
    ] + cmd)

def main_menu():
    while True: 
        os.system('clear')
        console.print(("[bold cyan]\n\n  Welcome to Nomi!\n\n[/]"))

        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Open/Create Chat",
                "Delete Chat",
                "Change Default Model",
                "Edit Persona",
                "Exit"
            ],
            qmark=" ❯ "
        ).ask()

        if choice == "Open/Create Chat":
            chat_name = choose_chat()
            if chat_name is None:
                continue
            launch_chat_window(chat_name)
        if choice == "Delete Chat":
            dl_chat = delete_chat()
            if dl_chat is None:
                continue
            path = os.path.join(chat_dir, dl_chat + ".json")
            os.remove(path)
            console.print(f"[bold red]Deleted:[/] {dl_chat}")
            console.print(f"\n[italic gray]Press enter to continue...[/]\n")
            input()
        elif choice == "Change Default Model":
            edit_config(model=choose_model())
        elif choice == "Edit Persona":
            new_persona = edit_persona()
            if new_persona is not None:
                edit_config(persona=new_persona)
        elif choice == "Exit":
            os.system('clear')
            break      
