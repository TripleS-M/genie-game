from config import client, MODEL_NAME
from prompts import REGULAR_PROMPT, HARD_PROMPT, build_user_prompt
from utils import parse_response

def analyse_wish(wish, difficulty="regular", history=[]):
    sys_prompt = HARD_PROMPT if difficulty == "hard" else REGULAR_PROMPT
    messages = [{"role": "system", "content": sys_prompt}]

    for past_wish, past_response in history:
        messages.append({"role": "user", "content": build_user_prompt(past_wish)})
        messages.append({"role": "assistant", "content": str(past_response)})
    
    messages.append({"role": "user", "content": build_user_prompt(wish)})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.8,
        max_tokens=500,
        response_format={"type": "json_object"}
    )

    raw_text = response.choices[0].message.content
    parsed = parse_response(raw_text=raw_text)

    return parsed