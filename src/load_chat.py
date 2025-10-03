import os, json, questionary, sqlite3
from rich.console import Console
from rich.prompt import Prompt

console = Console()
# chat_dir = "chats"
# os.makedirs(chat_dir, exist_ok=True)
DB_NAME = "nomi_memory.db"
def list_chat_logs():
    """
    List all chats to choose from
    """
    # return [
    #     f[:-5] # to remove extension from the name
    #     for f in os.listdir(chat_dir)
    #     if f.endswith(".json")
    # ]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM chats ORDER BY created_at")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_chat_id_by_name(chat_name):
    """Get chat ID by name, creating the chat if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM chats WHERE name=?", (chat_name,))
    row = cursor.fetchone()
    if row:
        chat_id = row[0]
    else:
        cursor.execute("INSERT INTO chats (name) VALUES (?)", (chat_name,))
        chat_id = cursor.lastrowid
        conn.commit()
    conn.close()
    return chat_id

def choose_chat():
    chats = list_chat_logs()
    choices = ["Create new chat"] + chats + ["Back"]
    selected = questionary.select(
        " ",
        choices=choices,
        qmark=" ❯ "
    ).ask()

    if selected == "Create new chat":
        chat_name = questionary.text("Give your new chat a name: ").ask()
        chat_id = get_chat_id_by_name(chat_name)
        return chat_name, chat_id
    elif selected == "Back":
        return None, None

    chat_name = selected
    # path = os.path.join(chat_dir, chat_name + ".json")
    # with open(path, "r", encoding="utf-8") as f:
    #     history = json.load(f) or []
    chat_id = get_chat_id_by_name(chat_name)
    console.print(f"\nLoaded chat: [bold]{chat_name}[/]\n")
    return chat_name, chat_id

    """
    Old logic just for reference
    """
    # console.print("[bold green]Your saved chats:[/]")
    # for i, name in enumerate(chats, 1):
    #     console.print(f"[cyan]{i}.[/] {name}")
    # console.print(f"[cyan]{len(chats)+1}[/] Create new chat")
    
    # idx = Prompt.ask(
    #     "Enter number: ",
    #     choices=[str(i) for i in range(1, len(chats)+2)]
    # )
    # # if creating new chat
    # if int(idx) == len(chats) + 1:
    #     chat_name = Prompt.ask("Give it a name: ")
    #     history = []
    #     return chat_name, history

    # # if selecting existing chat
    # chat_name = chats[int(idx) - 1]
    # path = os.path.join(chat_dir, chat_name + ".json")
    # with open(path, "r", encoding="utf-8") as f:
    #     history = json.load(f) or []

    # console.print(f"\nLoaded chat: [bold]{chat_name}[/]\n")
    # return chat_name, history