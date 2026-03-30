# The Fine Print - AI Genie Wish Game

An AI-powered genie game where players try to outsmart a clever Large Language Model by making precise wishes.

You get 3 wishes. The genie will look for loopholes, ambiguity, and logical flaws in your wording depending on the difficulty selected. If your wish is poorly worded, the genie twists it. If it's airtight, you win!

## How It Works

1. You select a difficulty level (Regular or Hard)
2. You type a wish in plain English
3. The AI genie analyzes your wording for flaws
4. Flawed wish: the genie twists it and the Genie wins that round
5. Well-worded wish: it is granted and the Player wins that round
6. After 3 wishes, the final score and winner are revealed

## Screenshots

<img src="./images/start.png"  width="500">

<img src="./images/gameplay.png" width="500">

## Prerequisites

- Python 3.10+
- Groq API Key (Or OpenAI API Key if using an OpenAI model, default setup points to Groq's open-ai compatibility layer).

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/TripleS-M/genie-game.git
cd genie-game
```

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
cd ../frontend
pip install -r requirements.txt
```

### 4. Configure your API key

Create or edit the file `backend/.env` with your API key:

```
API_KEY=gsk-your-api-key-here
```

## Running the Game

You need two active terminals running simultaneously:

### Terminal 1 - Background Server

```bash
cd backend
python main.py
```

### Terminal 2 - Game Client

```bash
cd frontend
python main.py
```

A Pygame window will open and initiate the game.

## Controls

Action | Key
--- | ---
Select Difficulty | Up / Down Arrows
Submit / Start / Continue | Enter
Quit | Close Window

## Project Structure

genie-game/
- backend/
  - main.py (FastAPI server containing /wish endpoint)
  - genie.py (OpenAI model integration and logic)
  - prompts.py (System prompt files and context tuning)
  - config.py (Configuration and keys)
- frontend/
  - main.py (Pygame game loop)
  - ui.py (User Interface rendering constraints)
  - game_state.py (State machines)
  - api.py (Communication with backend API)
  - settings.py (Color tokens and constants)
- README.md

## Tips for Outsmarting the Genie

- Be highly specific regarding quantities, currencies, and timeframes
- Think hard about any missing clauses or loopholes that an AI model can exploit
- Choose normal difficulty if you're finding it too difficult to constrain the model

## License
Created for Hackiethon.
