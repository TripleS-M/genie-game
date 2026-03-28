from config import MAX_WISHES

class GameState:
    def __init__(self):
        self.wishes_remaining = MAX_WISHES
        self.history = []
        self.score = 0
        self.wishes_made = 0

    
    def add_wish(self, wish, result):
        self.history.append((wish, result))
        if result["verdict"] == "granted":
            self.score += 1

        self.wishes_made += 1
        self.wishes_remaining -= 1


    def is_game_over(self):
        return self.wishes_remaining == 0

    def get_summary(self):
        if self.score == 0:
            performance = "bozo"
        elif self.score == 1:
            performance = "only one"
        elif self.score == 2:
            performance = "not bad"
        elif self.score == 3:
            performance = "goat"
        
        return {
            "score": self.score,
            "wishes_made": self.wishes_made,
            "performance": performance,
            "history": self.history
        }