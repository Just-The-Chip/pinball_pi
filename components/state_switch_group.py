from components.state_switch import StateSwitch
from components.util import HandlerResponse


class StateSwitchGroup:

    def __init__(self, **kwargs) -> None:
        self.state_group = kwargs.pop("state_group")

        target_settings: list[dict] = kwargs.pop("target_settings")
        self.target_ids: list[int] = [target.get("component_id") for target in target_settings]

        target_points: int = kwargs.pop("target_points", 0)
        self.targets: list[StateSwitch] = []
        self.build_targets(target_settings, target_points)

    def build_targets(self, target_settings: list[dict], target_points: int):
        for index, target in enumerate(target_settings):
            light_group_id = target.get("light_group_id")
            pattern_id = target.get("pattern_id", 2)
            variant_id = target.get("variant_id", 3)
            points = target.get("points") or target_points
            self.targets.append(
                StateSwitch(
                    state_key=(self.state_group, index),
                    toggle=False,
                    points_value=points,
                    light_group_id=light_group_id,
                    pattern_id=pattern_id,
                    variant_id=variant_id
                )
            )

    def register_message_handlers(self, game):
        for index, target_id in enumerate(self.target_ids):
            target = self.targets[index]
            game.register_message_handler(target_id, target.handle_message)

    def is_group_fully_triggered(self, gameState):
        return self.triggered_count(gameState) == len(self.targets)

    def triggered_count(self, gameState):
        state = gameState.get_state(self.state_group, {})

        num_triggered = 0
        for index in range(len(self.targets)):
            if state.get(index, False):
                num_triggered += 1

        return num_triggered

    def shift_state_group(self, gameState, reverse=False):
        result_queue = HandlerResponse()

        triggered_count = self.triggered_count(gameState)
        if triggered_count == 0 or triggered_count == len(self.targets):
            return result_queue

        state_list = [gameState.get_state((self.state_group, i), False) for i in range(len(self.targets))]

        print(f"{str(self.state_group)} OLD State: {str(state_list)}")

        if reverse:
            state_list.append(state_list.pop(0))
        else:
            state_list.insert(0, state_list.pop(len(state_list) - 1))

        for index, target in enumerate(self.targets):
            gameState.set_state((self.state_group, index), state_list[index])
            result_queue.extend(target.build_light_message(gameState))

        print(f"{str(self.state_group)} NEW State: {str(gameState.get_state(self.state_group, {}))}")

        return result_queue

    def activate_state_group(self, gameState):
        result_queue = HandlerResponse()
        for target in self.targets:
            result_queue.extend(target.activate_state(gameState))

        return result_queue

    def reset_state_group(self, gameState):
        result_queue = HandlerResponse()
        for target in self.targets:
            result_queue.extend(target.reset_state(gameState))

        return result_queue
