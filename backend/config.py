import os
from dotenv import load_dotenv
from openai import OpenAI

# loading the env file
load_dotenv()

# constants
API_KEY = os.getenv("API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_WISHES = 3

# Groq API base URL (gsk_ key = Groq, not OpenAI)
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# checks if api key not found in env file
if not API_KEY:
    raise ValueError("api key not in .env file")

# create the client (OpenAI-compatible, pointed at Groq)
client = OpenAI(
    api_key=API_KEY,
    base_url=GROQ_BASE_URL,
)
