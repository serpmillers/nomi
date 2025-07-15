#cli 
import signal, shutil
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.patch_stdout import patch_stdout

session = PromptSession()

def get_user_input():
    return session.prompt()
