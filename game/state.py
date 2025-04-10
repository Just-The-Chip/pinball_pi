import copy
from time import time


class State:

    def __init__(self) -> None:
        self.balls_remaining = 3
        self.balls_in_play = 0
        self.ball_save_time = 0
        self.score = 0

        self.multipliers = {
            "plinko": 0
        }

        self.previous_state_data = {}

        self.state_data = {
            "mag_bridge_is_traveling": False,
            "mag_bridge_is_active": False,
            "mag_bridge_error": False,
            "mag_bridge_switches": {},
            "slider_progress": 0,
            "slider_timestamp": 0
        }

        self.drop_target_groups = {
            "test_group": {
                1: 0,
                2: 0,
                3: 0
            }
        }

    def stacked_multiplier(self):
        multiplier = 1
        for value in self.multipliers.values():
            multiplier += value

        return multiplier

    def add_points(self, points):
        self.score = self.score + points * self.stacked_multiplier()
        print(f"Points: {self.stacked_multiplier()} x {points} -> {self.score}")

    def add_balls_in_play(self, balls=1):
        self.balls_in_play += balls

    def reduce_balls_in_play(self, balls=1):
        self.balls_in_play -= balls

    def add_balls_remaining(self, balls=1):
        self.balls_remaining += balls

    def reduce_balls_remaining(self, balls=1):
        self.balls_remaining -= balls

    def enable_ball_save(self, time_limit):
        new_save_time = (time() * 1000) + time_limit
        if (new_save_time > self.ball_save_time):
            self.ball_save_time = new_save_time

    def disable_ball_save(self):
        self.ball_save_time = 0

    def set_drop_target(self, group_id, target_id, value):
        if group_id not in self.drop_target_groups:
            self.drop_target_groups[group_id] = {}

        self.drop_target_groups[group_id][target_id] = value

    def drop_target_group(self, group_id):
        return self.drop_target_groups.get(group_id, {})

    def set_multiplier(self, multiplier_name, value):
        self.multipliers[multiplier_name] = value

    def reset_multipliers(self):
        for multiplier_name in self.multipliers:
            self.multipliers[multiplier_name] = 0

    # may refactor to have drop targets just use this instead but for now they are separate
    def set_state(self, keys, value):
        keys = [keys] if isinstance(keys, str) else list(keys)
        if len(keys) < 1:
            raise ValueError('must provide key')

        parent = self.state_data
        key_count = len(keys)
        while key_count > 0:
            next_key = keys.pop(0)
            key_count = len(keys)
            if key_count == 0:
                parent[next_key] = value
            else:
                if next_key not in parent:
                    parent[next_key] = {}
                parent = parent[next_key]

    def get_state(self, keys, default, getPrevious=False):
        keys = [keys] if isinstance(keys, str) else list(keys)
        if len(keys) < 1:
            raise ValueError('must provide key')

        state_dic = self.previous_state_data if getPrevious else self.state_data
        val = state_dic
        for key in keys:
            if key not in val:
                return default

            val = val[key]
        return val

    def get_state_change(self, keys, default):
        return {
            "from": self.get_state(keys, default, True),
            "to": self.get_state(keys, default)
        }

    def has_state_changed(self, keys, default):
        change = self.get_state_change(keys, default)
        return change["from"] is not change["to"]

    def commit_changes(self):
        self.previous_state_data = copy.deepcopy(self.state_data)
