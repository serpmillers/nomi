# 🧠 Nomi – Your AI Assistant with Memory

Nomi is a smart, cli-based AI assistant designed for local interaction using Google's Gemini API. It remembers your chats, supports multiple sessions like ChatGPT, and is built with personality.

---

## 🚀 Features

- ✅ Supports Gemini models (`gemini-1.5-flash-002`, etc.)
- 💬 Multi-session chat (like ChatGPT)
- 📁 Stores chat logs in `/chats` folder
- 🧠 Persona-driven responses
- 🌐 CLI-powered interface using `rich`

### Planned features:
- Allowing other users to join in a chat for working together
- Web Scraping
- File support
- Chat exporter
- Better cli formatting
- Full terminal integration
- Voice capabilities

---

## 📁 Folder Structure

```
nomi/
│
├── chats/              # Chat history (in .json format)
├── src/
│   ├── brain.py        # Handles the chat loop
│   ├── load_chat.py    # Manages loading chat history
│   ├── menu.py         # Menu for accessing the bot's features
│   ├── startup.py      # Handles Model selection (not in use)
│   └── utils/
│       └── cli.py      # Handles CLI inputs
│
├── nomi.py             # Entry point
├── config.yaml         # Configuration file for persona & model
├── requirements.txt    # All required Python packages
├── .env                # Gemini API key (not tracked by git)
└── README.md           

```
