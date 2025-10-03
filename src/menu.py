#loading menu trial

import os, yaml, questionary, subprocess, platform, shutil, sys, psutil
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
TERMINAL_CANDIDATES_LINUX = {
    "gnome-terminal",
    "alacritty",
    "kitty",
    "wezterm",
    "xterm",
    "foot",
    "tilix",
    "konsole",
    "lxterminal",
    "xfce4-terminal",
    "urxvt",
}
TERMINAL_CANDIDATES_MAC = {
    "iTerm.app",
    "Terminal.app"
}
TERMINAL_CANDIDATES_WIN = {
    "wt",
    "powershell",
    "cmd"
}

console = Console()
chat_dir = "chats"

def get_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        # Create default config if it doesn't exist
        default_config = {"default_model": "gemini-1.5-flash", "persona": ""}
        with open(CONFIG_PATH, "w") as f:
            yaml.dump(default_config, f)
        return default_config

def center(text):
    return Align.center(Panel(text, expand=False))

def get_python_executable():
    system = platform.system().lower()
    if system == "windows":
        return sys.executable or "python"
    else:
        return "python3"

def clear_console():
    system = platform.system().lower()
    if system == "linux" or system == "darwin":
        os.system('clear')
    elif system == "windows":
        os.system('cls')

def detect_current_terminal():
    """
    Detects the terminal that is running this process.
    Returns the terminal executable name (like 'kitty', 'gnome-terminal', 'cmd.exe', 'powershell.exe'),
    or None if not found.
    """
    try:
        parent = psutil.Process(os.getppid())  # parent process of the Python script
        term = parent.name().lower()

        # Normalize known cases
        if "gnome-terminal" in term:
            return "gnome-terminal"
        elif "kitty" in term:
            return "kitty"
        elif "alacritty" in term:
            return "alacritty"
        elif "wezterm" in term:
            return "wezterm"
        elif "powershell" in term:
            return "powershell"
        elif "cmd.exe" in term:
            return "cmd.exe"
        elif "windowsterminal" in term:
            return "wt"  # Windows Terminal CLI

        return term  # fallback: return the raw parent process name
    except Exception:
        return None

def detect_terminal():
    cfg = get_config()
    system = platform.system().lower()
    
    # Check if we have a configured terminal AND it actually exists
    if "default_terminal" in cfg and cfg["default_terminal"]:
        configured_terminal = cfg["default_terminal"]
        
        # Verify the configured terminal actually exists
        terminal_exists = False
        if system == "linux":
            terminal_exists = shutil.which(configured_terminal) is not None
        elif system == "darwin":
            if configured_terminal.endswith(".app"):
                terminal_exists = os.path.exists(f"/Applications/{configured_terminal}")
            else:
                terminal_exists = shutil.which(configured_terminal) is not None
        elif system == "windows":
            terminal_exists = shutil.which(configured_terminal) is not None
        
        # if terminal_exists:
        #     console.print(f"[green]Using configured terminal:[/] {configured_terminal}")
        #     return configured_terminal
        # else:
        #     console.print(f"[yellow]Configured terminal '{configured_terminal}' not found, auto-detecting...[/]")
        #     # Continue to auto-detection below

    # Auto-detect available terminal
    detected_terminal = None

    if system == "linux":
        for term in TERMINAL_CANDIDATES_LINUX:
            if shutil.which(term):
                detected_terminal = term
                break
    elif system == "darwin":
        for term in TERMINAL_CANDIDATES_MAC:
            app_path = f"/Applications/{term}"
            if os.path.exists(app_path):
                detected_terminal = term
                break
    elif system == "windows":
        for term in TERMINAL_CANDIDATES_WIN:
            if shutil.which(term):
                detected_terminal = term
                break

    if detected_terminal:
        # Update config with the newly detected terminal
        # edit_config(terminal=detected_terminal)
        # console.print(f"[green]Detected and saved terminal:[/] {detected_terminal}")
        return detected_terminal
    else:
        # console.print("[red]No supported terminal found. Please install one or manually set default_terminal in config.yaml[/]")
        return None
    
def edit_config(model=None, persona=None, terminal=None):
    # with open(CONFIG_PATH, "r") as f:
    #     cfg = yaml.safe_load(f)
    cfg = get_config()
    if model: cfg["default_model"] = model
    if persona is not None: cfg["persona"] = persona
    if terminal: cfg["default_terminal"] = terminal
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f)

# def choose_model():
#     model = questionary.select(
#         "Pick a Gemini model:",
#         choices = [f"{m} - {desc}" for m, desc in MODELS.items()
#         ],
#         qmark=" ❯ "
#     ).ask()
#     return model.split(" ")[0]

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
    terminal = detect_terminal()  # detect_terminal()

    if not terminal:
        console.print("[red]No terminal available. Cannot launch chat window.[/]")
        return
    python_exec = get_python_executable()
    cmd = [python_exec, "-m", "src.brain", chat_name]
    system = platform.system().lower()

    try:
        if system == "linux":
            if terminal in ["kitty", "alacritty"]:
                args = [terminal, "--title", f"Nomi – {chat_name}", "--"] + cmd
            elif terminal == "wezterm":
                args = [terminal, "start", "--", "bash", "-c", " ".join(cmd)]
            elif terminal == "gnome-terminal":
                args = [terminal, "--title", f"Nomi – {chat_name}", "--"] + cmd
            elif terminal in ["xfce4-terminal", "tilix"]:
                args = [terminal, "--title", f"Nomi – {chat_name}", "-e", " ".join(cmd)]
            elif terminal == "konsole":
                args = [terminal, "--new-tab", "-p", f"tabtitle=Nomi – {chat_name}", "-e"] + cmd
            elif terminal == "xterm":
                args = [terminal, "-T", f"Nomi – {chat_name}", "-e"] + cmd
            elif terminal == "foot":
                args = [terminal, "--title", f"Nomi – {chat_name}"] + cmd
            else:
                args = [terminal, "-e"] + cmd
            
            subprocess.Popen(args)

        elif system == "darwin":
            cmd_str = " ".join([f'"{arg}"' if " " in arg else arg for arg in cmd])
            if terminal == "iTerm.app":
                applescript = f'''
                tell application "iTerm"
                    create window with default profile
                    tell current session of current window
                        write text "{cmd_str}"
                        set name to "Nomi – {chat_name}"
                    end tell
                end tell
                '''
                subprocess.Popen(["osascript", "-e", applescript])
            else:  # Terminal.app
                applescript = f'''
                tell application "Terminal"
                    do script "{cmd_str}"
                    set custom title of front window to "Nomi – {chat_name}"
                end tell
                '''
                subprocess.Popen(["osascript", "-e", applescript])

        elif system == "windows":
            cmd = [python_exec, "-m", "src.brain", chat_name]
            
            subprocess.run(cmd)
            subprocess.run([python_exec, "-m", "src.menu"])
            # sys.exit(0) 

    except FileNotFoundError:
        console.print(f"[red]Terminal '{terminal}' not found![/]")
    except Exception as e:
        console.print(f"[red]Error launching terminal: {e}[/]")

def main_menu():
    while True:
        system = platform.system().lower()
        clear_console()
        console.print(("[bold cyan]\n\n  Welcome to Nomi!\n\n[/]"))

        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Open/Create Chat",
                "Delete Chat",
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
        # elif choice == "Change Default Model":
        #     edit_config(model=choose_model())
        elif choice == "Edit Persona":
            new_persona = edit_persona()
            if new_persona is not None:
                edit_config(persona=new_persona)
        elif choice == "Exit":
            clear_console()
            break      
