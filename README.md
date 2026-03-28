# 🧞 The Fine Print — AI Genie Wish Game

An AI-powered genie game where players try to outsmart a clever LLM by making precise wishes.

You get **3 wishes**. The genie will look for loopholes, ambiguity, and logical flaws in your wording. If your wish is poorly worded, the genie twists it. If it's airtight, you win!

---

## 🎮 How It Works

1. You type a wish in plain English
2. The AI genie analyzes your wording for flaws
3. **Flawed wish** → the genie twists it (Genie Wins)
4. **Well-worded wish** → it's granted (Player Wins)
5. After 3 wishes, the final score is revealed

---

## 📋 Prerequisites

- **Python 3.10+**
- **OpenAI API Key** — Get one at [platform.openai.com](https://platform.openai.com/)

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/TripleS-M/genie-game.git
cd genie-game
```

### 2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Install frontend dependencies

```bash
pip install -r frontend/requirements.txt
```

### 4. Configure your OpenAI API key

Create or edit the file `backend/.env`:

```
OPENAI_API_KEY=sk-your-api-key-here
```

> ⚠️ **Never commit your API key to version control.** The `.env` file is already in `.gitignore`.

---

## ▶️ Running the Game

You need **two terminals** running at the same time:

### Terminal 1 — Start the backend server

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 — Launch the game

```bash
cd frontend
python main.py
```

A Pygame window will open with the game.

---

## 🕹️ Controls

| Action | Key |
|--------|-----|
| Start game | `Enter` |
| Type your wish | Keyboard |
| Submit wish | `Enter` |
| Continue after result | `Enter` |
| Play again (after game over) | `Enter` |
| Quit | Close window |

---

## 🏗️ Project Structure

```
genie-game/
├── backend/
│   ├── main.py            # FastAPI server with /wish endpoint
│   ├── utils.py           # OpenAI integration & wish processing
│   ├── requirements.txt   # Backend dependencies
│   └── .env               # API key (not committed)
│
├── frontend/
│   ├── main.py            # Pygame game loop
│   ├── ui.py              # UI rendering (dialogue, input, genie)
│   ├── game_state.py      # Game state machine
│   ├── api.py             # Async API communication
│   ├── settings.py        # Constants & configuration
│   ├── requirements.txt   # Frontend dependencies
│   └── assets/
│       └── images/        # Genie state images
│
└── README.md
```

---

## 🛠️ Tech Stack

- **Frontend:** Python, Pygame
- **Backend:** Python, FastAPI, Uvicorn
- **AI:** OpenAI API (GPT-4o-mini)

---

## 📝 Tips for Outsmarting the Genie

- Be **specific** — specify quantities, currencies, timeframes
- Cover **edge cases** — "with no negative consequences to anyone"
- Avoid **ambiguity** — don't use words with multiple meanings
- Think about **how** the wish could be fulfilled maliciously

---

## 📄 License

This project was built for the Hackiethon hackathon.
