import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set in environment!")

genai.configure(api_key=api_key)

# Hardcoded generateContent models list (no ranking)
generate_models_list = [
    # "gemma-3-27b-it",
    # "gemma-3-12b-it",
    # "gemma-3-4b-it",
    # "gemma-3-1b-it",
    # "gemma-3n-e4b-it",
    # "gemma-3n-e2b-it",
    # "gemini-pro-latest",
    # "gemini-flash-latest",
    # "gemini-flash-lite-latest",
    # "gemini-2.5-pro",
    # "gemini-2.5-pro-preview-06-05",
    # "gemini-2.5-pro-preview-05-06",
    # "gemini-2.5-pro-preview-03-25",
    "gemini-2.5-flash",
    "gemini-2.5-flash-preview-09-2025",
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-lite-preview-09-2025",
    "gemini-2.5-flash-lite-preview-06-17",
    "gemini-2.0-pro-exp-02-05",
    "gemini-2.0-pro-exp",
    "gemini-2.0-flash-thinking-exp-1219",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite-001",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-preview-image-generation",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-2.0-flash-lite-preview",
    "gemini-exp-1206",
    "gemini-2.5-flash-preview-tts",
    "gemini-2.5-pro-preview-tts",
    "learnlm-2.0-flash-experimental",
    "gemini-2.5-flash-image",
    "gemini-2.5-flash-image-preview",
    "gemini-robotics-er-1.5-preview"
]

def get_working_model(persona):
    """
    Returns the first working model from the hardcoded list.
    """
    for model_name in generate_models_list:
        try:
            test_model = genai.GenerativeModel(model_name, system_instruction=persona)
            test_model.start_chat(history=[])  # test availability
            return model_name  # first working model
        except Exception:
            continue

    # fallback if none work
    return "gemini-2.5-flash"
