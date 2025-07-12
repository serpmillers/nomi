#!/usr/bin/env python3

#main file, links to terminal

import os
import yaml
from dotenv import load_dotenv
from rich.console import Console
from src.utils.cli import get_user_input
from src.brain import Brain
from src.startup import Startup

load_dotenv()
console = Console()

CONFIG_PATH = "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

Startup(config_path=CONFIG_PATH).run()
brain = Brain(config)

def main():
    while True:
        user_input= get_user_input()
        if user_input.lower() in ["exit", "quit", "bye"]:
            console.print("[italic dim]Goodbye, human. See you later[/italic dim]")
            break

        response = brain.generate_response(user_input)
        console.print(f"[bold green]Nomi:[/] {response}")

if __name__ == "__main__":
    main()