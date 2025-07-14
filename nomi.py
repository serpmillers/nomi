#!/usr/bin/env python3

#main file, links to terminal

import os, yaml, subprocess, platform
from contextlib import contextmanager
from dotenv import load_dotenv
from rich.console import Console
from src.brain import Brain
from src.startup import Startup
from src import menu

class Nomi:
    def __init__(self):
        load_dotenv()
        self.console = Console()

        self.CONFIG_PATH = "config.yaml"
        with open(self.CONFIG_PATH, "r") as f:
            self.config = yaml.safe_load(f)

    # didn't use because shifted to separate terminal windows for chats

    # @contextmanager
    # def alternate_screen(self):
    #     """
    #     This is so that nomi can look like it's own instance
    #     """
    #     os.system("tput smcup")
    #     os.system("clear")
    #     try:
    #         yield
    #     finally:
    #         os.system("clear")
    #         os.system("tput rmcup")

    def main(self):
        
        Startup(config_path=self.CONFIG_PATH).run()
        brain = Brain(self.config)

        brain.chat()

if __name__ == "__main__":
    
    menu.main_menu()