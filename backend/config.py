import os
from dotenv import load_dotenv
from openai import OpenAI

# loading the env file
load_dotenv()

# constants
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_WISHES = 3


# checks if api key not found in env file
if not API_KEY:
    raise ValueError("api key not in .env file")

# create the client
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# tests if the file is working
if __name__ == "__main__":
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "say hello"}]
    )

    print(response.choices[0].message.content)