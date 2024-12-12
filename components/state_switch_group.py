from components.state_switch import StateSwitch


class StateSwitchGroup:

    def __init__(self, **kwargs) -> None:
        self.state_group = kwargs.pop("state_group")

        target_settings = kwargs.pop("target_settings")
        self.target_ids = [target.get("component_id") for target in target_settings]

        target_points = kwargs.pop("target_points", 0)
        self.targets = []
        self.build_targets(target_settings, target_points)

    def build_targets(self, target_settings, target_points):
        for index, target in enumerate(target_settings):
            light_group_id = target.get("light_group_id")
            points = target.get("points") or target_points
            self.targets.append(
                StateSwitch(
                    state_key=(self.state_group, index),
                    toggle=False,
                    points_value=points,
                    light_group_id=light_group_id
                )
            )

    def register_message_handlers(self, game):
        for index, target_id in enumerate(self.target_ids):
            target = self.targets[index]
            game.register_message_handler(target_id, target.handle_message)

    def is_group_fully_triggered(self, gameState):
        state = gameState.get_state(self.state_group, {})

        total_state = True
        for index in range(len(self.targets)):
            total_state = total_state and state.get(index, False)

        return total_state

    # def shift_state_group(self, gameState, reverse=False):
    #     current_state = gameState.get_state(self.state_group, {}).copy
    #     result_queue = []
    #     direction = -1 if reverse else 1

    #     for index, target in enumerate(self.targets):
    #         previous_key = index - direction
    #         current_state = gameState.get_state((self.state_group, index), False)
    #         gameState.set_state((self.state_group, index), previous_state)
    #         previous_state = current_state
    #         result_queue.extend(target.build_light_message(gameState))

    #     return result_queue

    def reset_state_group(self, gameState):
        result_queue = []
        for index, target in enumerate(self.targets):
            gameState.set_state((self.state_group, index), False)
            result_queue.extend(target.build_light_message(gameState))

        return result_queue
