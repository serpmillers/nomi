#cli 
from prompt_toolkit import PromptSession

session = PromptSession()

def get_user_input():
    return session.prompt()