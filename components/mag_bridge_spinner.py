from comm.constants import COMM_SOLENOIDS
from comm.util import build_component_message
from data.constants import MAG_BRIDGE_TRAVELING_KEY, MAG_BRIDGE_ERROR_KEY


class MagBridgeSpinner:
    def __init__(self, **kwargs):
        self.spinner_id = kwargs.pop("spinner_id")

    def start_spinner(self):
        return [(COMM_SOLENOIDS, build_component_message(self.spinner_id, 1))]

    def stop_spinner(self):
        return [(COMM_SOLENOIDS, build_component_message(self.spinner_id, 0))]

    def handle_magbridge_complete(self, gameState):
        bridge_is_traveling = gameState.get_state_change(MAG_BRIDGE_TRAVELING_KEY, False)

        if bridge_is_traveling["from"] == True and bridge_is_traveling["to"] == False:
            print(f"Start that spinner!")

            if gameState.get_state(MAG_BRIDGE_ERROR_KEY, False):
                print("The mag bridge has errored out. Restart to attempt to fix it.")
            else:
                return self.start_spinner()

        return []

    def handle_spinner_stop(self, _message, _gameState):
        return self.stop_spinner()

    def handle_cleanup(self, _gameState):
        return self.stop_spinner()
