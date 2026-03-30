import os
from dotenv import load_dotenv
from openai import OpenAI

# loading the env file
load_dotenv()

# constants
API_KEY = os.getenv("API_KEY")
MODEL_NAME = "gpt-4o-mini"
MAX_WISHES = 3


# checks if api key not found in env file
if not API_KEY:
    raise ValueError("api key not in .env file")

# create the client
client = OpenAI(
    api_key=API_KEY
)
