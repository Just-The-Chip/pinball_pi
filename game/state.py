class State:
    balls_remaining = 3
    score = 0

    drop_target_groups = {
        "test_group": {
            1: 0,
            2: 0,
            3: 0
        }
    }

    def __init__(self) -> None:
        pass

    def stacked_multiplier(self):
        # over time as we think of more multipliers, this function will calculate the total
        # multiplier based on which ones are active
        return 1

    def add_points(self, points):
        self.score = self.score + points * self.stacked_multiplier()
        print(f"Points: {self.score}")

    def set_drop_target(self, group_id, target_id, value):
        if group_id not in self.drop_target_groups:
            self.drop_target_groups[group_id] = {}

        self.drop_target_groups[group_id][target_id] = value

    def drop_target_group(self, group_id):
        return self.drop_target_groups.get(group_id, {})
