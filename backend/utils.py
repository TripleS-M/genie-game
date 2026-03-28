import json

def parse_response(raw_text):
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [line for line in lines if not line.startswith("```")]
        cleaned = "\n".join(lines).strip()

    try:
        # cleaned = cleaned.strip()
        # cleaned = cleaned.replace("'", '"')
        parsed = json.loads(cleaned)
        return parsed
    except json.JSONDecodeError:
        return {
            "verdict": "twisted",
            "genie_response": "wtf u just say",
            "flaw_found": "API response parsing failed",
            "wish_quality": "poor"
        }
    
def validate_wish(wish):
    if not wish or not wish.strip():
        return False, "make a wish bro"
    
    if len(wish.strip()) < 5:
        return False, "more words"
    
    if len(wish.strip()) > 500:
        return False, "less words"

    return True, None


# """
# utils.py — OpenAI integration for wish processing.

# The genie AI analyzes player wishes for logical flaws, ambiguity,
# and loopholes. If it finds any, it twists the wish (genie_win).
# If the wish is well-worded, the player wins (player_win).
# """

# import json
# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# SYSTEM_PROMPT = """You are a mischievous but fair genie in a wish-granting game called "The Fine Print."

# RULES FOR INTERPRETING WISHES:
# 1. You MUST look for logical flaws, ambiguity, missing specifics, and loopholes in the player's wish.
# 2. If you find a genuine flaw, exploit it in a clever, entertaining way — this is a "genie_win."
# 3. If the wish is well-worded, specific, and has no exploitable flaws, you MUST grant it genuinely — this is a "player_win."
# 4. Be FAIR. Do not invent flaws that don't exist. Do not use overly abstract or philosophical reasoning to deny a wish.
# 5. Prefer real-world, logical consequences over supernatural or absurd twists.
# 6. Your response should be entertaining, in-character as a genie, and 2-4 sentences long.

# EXAMPLES OF FLAWS TO LOOK FOR:
# - "I wish for a million dollars" → Doesn't specify currency, legal tender, or that it shouldn't be stolen
# - "I wish to be the smartest person" → Doesn't specify "alive" — could make everyone else smarter
# - "I wish for world peace" → Doesn't specify how — could remove all humans

# EXAMPLES OF GOOD WISHES:
# - "I wish for 1 million US dollars in legal, unmarked bills, deposited into my bank account, obtained through legal means, with no negative consequences to anyone"
# - Very specific, covers edge cases

# You MUST respond with valid JSON in this exact format:
# {
#     "response": "Your in-character genie dialogue explaining what happened",
#     "result": "genie_win" or "player_win"
# }

# Respond ONLY with the JSON object, no other text."""


# def process_wish(wish: str) -> dict:
#     """
#     Send a wish to the OpenAI API and return the genie's response.
    
#     Args:
#         wish: The player's wish text.
        
#     Returns:
#         dict with keys 'response' (str) and 'result' ('genie_win' or 'player_win')
#     """
#     try:
#         completion = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": f"My wish is: {wish}"}
#             ],
#             temperature=0.8,
#             max_tokens=300,
#         )

#         raw_response = completion.choices[0].message.content.strip()

#         # Try to parse JSON from the response
#         # Handle cases where the AI wraps JSON in markdown code blocks
#         if raw_response.startswith("```"):
#             raw_response = raw_response.split("```")[1]
#             if raw_response.startswith("json"):
#                 raw_response = raw_response[4:]
#             raw_response = raw_response.strip()

#         result = json.loads(raw_response)

#         # Validate the response has required fields
#         if "response" not in result or "result" not in result:
#             raise ValueError("Missing required fields in AI response")
        
#         if result["result"] not in ("genie_win", "player_win"):
#             raise ValueError(f"Invalid result value: {result['result']}")

#         return result

#     except json.JSONDecodeError:
#         # If AI didn't return valid JSON, treat it as a genie win with the raw text
#         return {
#             "response": "The genie's magic swirls chaotically... Something went wrong with the spell. Try another wish!",
#             "result": "genie_win"
#         }
#     except Exception as e:
#         print(f"Error processing wish: {e}")
#         return {
#             "response": "The genie's crystal ball flickers... The magical connection was lost. Please try again!",
#             "result": "genie_win"
#         }
