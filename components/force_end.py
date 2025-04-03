from comm.constants import COMM_LIGHTS
from comm.util import build_light_message


class ForceEnd:

    def handle_message(self, msg, gameState):
        gameState.balls_remaining = 0

        return []
