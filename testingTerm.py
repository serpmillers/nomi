import os, yaml, questionary, subprocess, platform, shutil
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()

def get_config():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        default_config = {"default_model": "gemini-1.5-flash", "persona": ""}
        with open("config.yaml", "w") as f:
            yaml.dump(default_config, f)
        return default_config

def debug_terminal_detection():
    """Debug function to see what terminals are available"""
    system = platform.system().lower()
    console.print(f"[blue]Detected OS:[/] {system}")
    
    if system == "linux":
        terminals = ["gnome-terminal", "alacritty", "kitty", "wezterm", "xterm", "foot", "tilix", "konsole", "lxterminal", "xfce4-terminal", "urxvt"]
        console.print("[blue]Checking Linux terminals:[/]")
        for term in terminals:
            if shutil.which(term):
                console.print(f"  ✓ {term} - FOUND at {shutil.which(term)}")
            else:
                console.print(f"  ✗ {term} - NOT FOUND")
                
    elif system == "darwin":
        terminals = ["iTerm.app", "Terminal.app"]
        console.print("[blue]Checking macOS terminals:[/]")
        for term in terminals:
            app_path = f"/Applications/{term}"
            if os.path.exists(app_path):
                console.print(f"  ✓ {term} - FOUND at {app_path}")
            else:
                console.print(f"  ✗ {term} - NOT FOUND at {app_path}")
                
    elif system == "windows":
        terminals = ["wt", "powershell", "cmd"]
        console.print("[blue]Checking Windows terminals:[/]")
        for term in terminals:
            if shutil.which(term):
                console.print(f"  ✓ {term} - FOUND at {shutil.which(term)}")
            else:
                console.print(f"  ✗ {term} - NOT FOUND")

def detect_terminal():
    cfg = get_config()
    if "default_terminal" in cfg and cfg["default_terminal"]:
        console.print(f"[green]Using configured terminal:[/] {cfg['default_terminal']}")
        return cfg["default_terminal"]

    system = platform.system().lower()
    console.print(f"[yellow]Auto-detecting terminal for {system}...[/]")
    
    detected_terminal = None

    if system == "linux":
        terminals = ["gnome-terminal", "alacritty", "kitty", "wezterm", "xterm", "foot", "tilix", "konsole", "lxterminal", "xfce4-terminal", "urxvt"]
        for term in terminals:
            if shutil.which(term):
                detected_terminal = term
                break
                
    elif system == "darwin":
        # Check for iTerm first, then Terminal
        if os.path.exists("/Applications/iTerm.app"):
            detected_terminal = "iTerm.app"
        elif os.path.exists("/Applications/Terminal.app"):
            detected_terminal = "Terminal.app"
            
    elif system == "windows":
        terminals = ["wt", "powershell", "cmd"]
        for term in terminals:
            if shutil.which(term):
                detected_terminal = term
                break

    if detected_terminal:
        # Save it to config
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f) or {}
        cfg["default_terminal"] = detected_terminal
        with open("config.yaml", "w") as f:
            yaml.dump(cfg, f)
        console.print(f"[green]Auto-detected and saved terminal:[/] {detected_terminal}")
        return detected_terminal
    else:
        console.print("[red]No supported terminal found![/]")
        return None

def test_terminal_launch(chat_name="test-chat"):
    """Test function to debug terminal launching"""
    terminal = detect_terminal()
    
    if not terminal:
        console.print("[red]Cannot test - no terminal detected[/]")
        return
        
    console.print(f"[blue]Testing launch with terminal:[/] {terminal}")
    
    # Simple test command instead of the actual chat
    test_cmd = ["echo", "Hello from Nomi!", "&&", "read", "-p", "Press enter to close..."]
    system = platform.system().lower()
    
    console.print(f"[blue]System:[/] {system}")
    console.print(f"[blue]Test command:[/] {' '.join(test_cmd)}")

    try:
        if system == "linux":
            if terminal == "gnome-terminal":
                args = ["gnome-terminal", "--title", f"Nomi Test – {chat_name}", "--", "bash", "-c", " ".join(test_cmd)]
            elif terminal == "alacritty":
                args = ["alacritty", "--title", f"Nomi Test – {chat_name}", "-e", "bash", "-c", " ".join(test_cmd)]
            elif terminal == "kitty":
                args = ["kitty", "--title", f"Nomi Test – {chat_name}", "bash", "-c", " ".join(test_cmd)]
            elif terminal == "xterm":
                args = ["xterm", "-T", f"Nomi Test – {chat_name}", "-e", "bash", "-c", " ".join(test_cmd)]
            else:
                # Fallback for other terminals
                args = [terminal, "-e", "bash", "-c", " ".join(test_cmd)]
            
            console.print(f"[blue]Launch command:[/] {' '.join(args)}")
            subprocess.Popen(args)
            console.print("[green]Terminal launched successfully![/]")

        elif system == "darwin":
            test_cmd_str = " ".join(test_cmd)
            if terminal == "iTerm.app":
                applescript = f'''
                tell application "iTerm"
                    activate
                    create window with default profile
                    tell current session of current window
                        write text "bash -c '{test_cmd_str}'"
                        set name to "Nomi Test – {chat_name}"
                    end tell
                end tell
                '''
            else:  # Terminal.app
                applescript = f'''
                tell application "Terminal"
                    activate
                    do script "bash -c '{test_cmd_str}'"
                    set custom title of front window to "Nomi Test – {chat_name}"
                end tell
                '''
            
            console.print(f"[blue]AppleScript:[/] {applescript}")
            subprocess.Popen(["osascript", "-e", applescript])
            console.print("[green]Terminal launched successfully![/]")

        elif system == "windows":
            test_cmd_str = " && ".join(test_cmd)
            if terminal == "wt":
                args = ["wt", "new-tab", "--title", f"Nomi Test – {chat_name}", "cmd", "/k", test_cmd_str]
            elif terminal == "powershell":
                args = ["powershell", "-NoExit", "-Command", test_cmd_str]
            else:  # cmd
                args = ["cmd", "/k", test_cmd_str]
            
            console.print(f"[blue]Launch command:[/] {' '.join(args)}")
            subprocess.Popen(args)
            console.print("[green]Terminal launched successfully![/]")

    except FileNotFoundError as e:
        console.print(f"[red]FileNotFoundError:[/] {e}")
        console.print(f"[red]Terminal '{terminal}' not found in PATH[/]")
    except Exception as e:
        console.print(f"[red]Error launching terminal:[/] {e}")

def launch_chat_window_fixed(chat_name):
    """Fixed version of launch_chat_window with better error handling"""
    terminal = detect_terminal()
    
    if not terminal:
        console.print("[red]No terminal available. Cannot launch chat window.[/]")
        return False
        
    cmd = ["python3", "-m", "src.brain", chat_name]
    system = platform.system().lower()
    
    console.print(f"[blue]Launching chat with:[/] {terminal}")
    console.print(f"[blue]Command:[/] {' '.join(cmd)}")

    try:
        if system == "linux":
            if terminal == "gnome-terminal":
                args = ["gnome-terminal", "--title", f"Nomi – {chat_name}", "--", "bash", "-c", f"{' '.join(cmd)}; exec bash"]
            elif terminal == "alacritty":
                args = ["alacritty", "--title", f"Nomi – {chat_name}", "-e", "bash", "-c", f"{' '.join(cmd)}; exec bash"]
            elif terminal == "kitty":
                args = ["kitty", "--title", f"Nomi – {chat_name}", "bash", "-c", f"{' '.join(cmd)}; exec bash"]
            elif terminal == "xterm":
                args = ["xterm", "-T", f"Nomi – {chat_name}", "-e", "bash", "-c", f"{' '.join(cmd)}; exec bash"]
            else:
                args = [terminal, "-e", "bash", "-c", f"{' '.join(cmd)}; exec bash"]
            
            subprocess.Popen(args)

        elif system == "darwin":
            cmd_str = " ".join(cmd)
            if terminal == "iTerm.app":
                applescript = f'''
                tell application "iTerm"
                    activate
                    create window with default profile
                    tell current session of current window
                        write text "{cmd_str}"
                        set name to "Nomi – {chat_name}"
                    end tell
                end tell
                '''
            else:  # Terminal.app
                applescript = f'''
                tell application "Terminal"
                    activate
                    do script "{cmd_str}"
                    set custom title of front window to "Nomi – {chat_name}"
                end tell
                '''
            
            subprocess.Popen(["osascript", "-e", applescript])

        elif system == "windows":
            if terminal == "wt":
                args = ["wt", "new-tab", "--title", f"Nomi – {chat_name}", "cmd", "/k"] + cmd
            elif terminal == "powershell":
                cmd_str = " ".join(cmd)
                args = ["powershell", "-NoExit", "-Command", cmd_str]
            else:  # cmd
                args = ["cmd", "/k"] + cmd
            
            subprocess.Popen(args)
            
        console.print("[green]Chat window launched successfully![/]")
        return True
        
    except FileNotFoundError:
        console.print(f"[red]Terminal '{terminal}' not found![/]")
        return False
    except Exception as e:
        console.print(f"[red]Error launching terminal:[/] {e}")
        return False

# Test functions you can call
if __name__ == "__main__":
    console.print("[bold cyan]Terminal Debug Tool[/]\n")
    
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Debug terminal detection",
            "Test terminal launch",
            "Launch actual chat window",
            "Exit"
        ]
    ).ask()
    
    if choice == "Debug terminal detection":
        debug_terminal_detection()
    elif choice == "Test terminal launch":
        test_terminal_launch()
    elif choice == "Launch actual chat window":
        chat_name = questionary.text("Chat name:").ask() or "test"
        launch_chat_window_fixed(chat_name)
    
    input("\nPress enter to exit...")
