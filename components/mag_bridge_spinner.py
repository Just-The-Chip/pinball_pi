from comm.constants import COMM_SOLENOIDS
from comm.util import build_component_message
from data.constants import IS_PLINKO_ACTIVE, MAG_BRIDGE_ERROR_KEY


class MagBridgeSpinner:
    def __init__(self, **kwargs):
        self.spinner_id = kwargs.pop("spinner_id")

    def start_spinner(self):
        return [(COMM_SOLENOIDS, build_component_message(self.spinner_id, 1))]

    def stop_spinner(self):
        return [(COMM_SOLENOIDS, build_component_message(self.spinner_id, 0))]

    def handle_plinko_complete(self, gameState):
        is_plinko = gameState.get_state_change(IS_PLINKO_ACTIVE, False)

        if is_plinko["from"] == True and is_plinko["to"] == False:
            print(f"Warm up that spinner!")

            if gameState.get_state(MAG_BRIDGE_ERROR_KEY, False):
                print("The mag bridge has errored out. Restart to attempt to fix it.")
            else:
                return self.start_spinner()

        return []

    def handle_spinner_stop(self, _message, _gameState):
        return self.stop_spinner()

    def handle_cleanup(self, _gameState):
        return self.stop_spinner()
