from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

def prompt_continuation(width, line_number, wrap_count):
    if wrap_count > 0:
        return " " * (width - 3) + "→ "
    else:
        text = ("- %i - " % (line_number + 1)).rjust(width)
        return HTML("<line-number>%s</line-number>" % text)

kb = KeyBindings()

@kb.add("c-m")
def _(event):
    """Submit"""
    buffer = event.current_buffer
    if buffer.validate():
        buffer.validate_and_handle()

@kb.add("c-\\")
def _(event):
    """Insert newline"""
    event.current_buffer.insert_text("\n")

# Custom style
custom_style = Style.from_dict({
    "prompt": "bold #b4befe",
    "line-number": "#b4befe",
})

session = PromptSession(key_bindings=kb, style=custom_style)

def get_user_input():
    return session.prompt(
        HTML("<prompt><b>You:</b></prompt> "),
        multiline=True,
        prompt_continuation=prompt_continuation
    )

