# 🧠 Nomi – Your AI Assistant with Memory

Nomi is a smart, cli-based AI assistant designed for local interaction using Google's Gemini API. It remembers your chats, supports multiple sessions like ChatGPT, and is built with personality.

---

## 🚀 Features

- ✅ Supports Gemini models (`gemini-1.5-flash-002`, etc.)
- 💬 Multi-session chat (like ChatGPT)
- 📁 Stores chat logs in `/chats` folder
- 🧠 Persona-driven responses
- 🌐 CLI-powered interface using `rich`

## Planned features:
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
│   ├── startup.py      # Handles Model selection (not in use right now)
│   └── utils/
│       └── cli.py      # Handles CLI inputs
│
├── nomi.py             # Entry point
├── config.yaml         # Configuration file for persona & model
├── requirements.txt    # All required Python packages
├── .env                # Gemini API key (not tracked by git)
└── README.md           

```
### 🛠 Instructions

## 1. **Clone the Repository**
Open your terminal or cmd and run:
```bash
git clone https://github.com/serpmillers/nomi
```
## 2. **Navigate into the Directory**
```bash
cd nomi                             # or wherever the repo has been cloned to
```
## 3. **Create and activate a virtual environment**
```bash
python3 -m venv .venv               # create the environment

source .venv/bin/activate           # activate it (Linux)
# OR
.venv\Scripts\activate              # activate it (Windows)
```
## 4. **Install Dependencies**
All the dependencies are written in a requirements.txt file, simply run:
```bash
pip install -r requirements.txt
```
## 5. **Set up Environment Variables**
create a `.env` file in the root directory with the following content:
```
GEMINI_API_KEY='your_api_key_goes_here'
```
> You can get your API key from: https://aistudio.google.com/app/apikey

## 6. **Finally, run it**
```bash
python3 nomi.py
```

## 7. **Tweak it according to your preference**
In the menu, you get the option to choose between different **models** of Gemini : from the fast and efficient ones to the heavyweights with top-tier reasoning. You can also edit the **persona**, customizing how Nomi behaves and responds. Whether you want a chill assistant, a sarcastic genius, or a medieval bard, it's all up to you.
---
**Nomi speaks your language — literally. Make it yours.**