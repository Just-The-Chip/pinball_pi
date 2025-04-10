from comm.constants import COMM_SERVOS
from comm.util import build_component_message


class DropTarget:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.pop("id")
        self.group_id = kwargs.pop("group_id")

    def handle_message(self, message, gameState):
        print(message)
        print(f"drop target {str(self.id)} fired!")
        if message > 0:
            gameState.set_drop_target(self.group_id, self.id, True)

        return []  # once lights is hooked up we can add message to send to lights


class DropTargetGroup:
    def __init__(self, **kwargs) -> None:
        self.targets = {}
        self.group_id = kwargs.pop("group_id")
        self.build_targets(kwargs.pop("target_ids"))

    def build_targets(self, target_ids):
        for target_id in target_ids:
            self.targets[target_id] = DropTarget(
                group_id=self.group_id, id=target_id)

    def register_message_handlers(self, game):
        for target_id, target in self.targets.items():
            game.register_message_handler(target_id, target.handle_message)

    def is_group_fully_triggered(self, gameState):
        state = gameState.drop_target_group(self.group_id)

        total_state = True

        for target_id in self.targets:
            total_state = total_state and state.get(target_id, False)

        return total_state

    def reset_if_all_triggered(self, gameState):
        if not self.is_group_fully_triggered(gameState):
            return []

        for target_id in self.targets:
            gameState.set_drop_target(self.group_id, target_id, False)

        return self.reset_targets()

    def reset_targets(self):
        result_queue = []

        for target_id in self.targets:
            message = build_component_message(target_id)
            result_queue.append((COMM_SERVOS, message))

        return result_queue
