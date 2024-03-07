# from comm.constants import COMM_SERVOS


class DropTarget:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.pop("id")
        self.group_id = kwargs.pop("group_id")

    def handle_message(self, message, gameState):
        if int.from_bytes(message, "big") > 0:
            gameState.set_drop_target(self.group_id, self.id, True)

        return []  # once lights is hooked up we can add message to send to lights


class DropTargetGroup:
    targets = {}

    def __init__(self, **kwargs) -> None:
        self.group_id = kwargs.pop("group_id")
        self.build_targets(kwargs.pop("target_ids"))

    def build_targets(self):
        for target_id in self.target_ids:
            self.targets[target_id] = DropTarget(
                group_id=self.group_id, id=target_id)

    def register_message_handlers(self, game):
        for target_id, target in self.targets:
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
            message = (target_id << 8) | 1
            result_queue.append(
                ("servos", message.to_bytes(2, "big") + b'\n'))

        return result_queue
