"""
main.py — FastAPI backend for The Fine Print genie game.

Provides the /wish endpoint that processes player wishes through OpenAI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import process_wish

app = FastAPI(title="The Fine Print - Genie Game API")

# Allow requests from the Pygame frontend (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WishRequest(BaseModel):
    wish: str


class WishResponse(BaseModel):
    response: str
    result: str  # "genie_win" or "player_win"


@app.get("/")
def root():
    return {"message": "The Fine Print - Genie Game API is running!"}


@app.post("/wish", response_model=WishResponse)
def make_wish(request: WishRequest):
    """
    Process a player's wish through the AI genie.
    
    The genie will analyze the wish for flaws and either:
    - Twist it (genie_win) if there are logical flaws
    - Grant it (player_win) if the wish is well-worded
    """
    if not request.wish.strip():
        raise HTTPException(status_code=400, detail="Wish cannot be empty!")

    result = process_wish(request.wish)
    return WishResponse(**result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
