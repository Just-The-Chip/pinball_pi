from comm.constants import COMM_SERVOS
from comm.util import build_component_message
from components.state_switch_group import StateSwitchGroup


class DropTargetGroup(StateSwitchGroup):
    def reset_if_all_triggered(self, gameState):
        if not self.is_group_fully_triggered(gameState):
            return []

        return self.reset_state_group(gameState)

    def reset_state_group(self, gameState):
        result_queue = super().reset_state_group(gameState)

        for target_id in self.target_ids:
            message = build_component_message(target_id)
            result_queue.append((COMM_SERVOS, message))

        return result_queue
