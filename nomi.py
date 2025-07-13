#!/usr/bin/env python3

#main file, links to terminal

import os
import yaml
from contextlib import contextmanager
from dotenv import load_dotenv
from rich.console import Console
from src.brain import Brain
from src.startup import Startup

class Nomi:
    def __init__(self):
        load_dotenv()
        self.console = Console()

        self.CONFIG_PATH = "config.yaml"
        with open(self.CONFIG_PATH, "r") as f:
            self.config = yaml.safe_load(f)
    
    @contextmanager
    def alternate_screen(self):
        """
        This is so that nomi can look like it's own instance
        """
        os.system("tput smcup")
        os.system("clear")
        try:
            yield
        finally:
            os.system("clear")
            os.system("tput rmcup")

    def main(self):
        
        Startup(config_path=self.CONFIG_PATH).run()
        brain = Brain(self.config)

        # new instance opens right after selecting model :)
        # with self.alternate_screen():

            # this is where the loop hides
        brain.chat()            

if __name__ == "__main__":
    Nomi().main()