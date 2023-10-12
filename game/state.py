class State:
    balls_remaining = 3
    score = 0

    def __init__(self) -> None:
        pass

    def stacked_multiplier(self):
        # over time as we think of more multipliers, this function will calculate the total 
        # multiplier based on which ones are active
        return 1

    def add_points(self, points):
        self.score = self.score + points * self.stacked_multiplier()