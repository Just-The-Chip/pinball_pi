from data.constants import LEFT_LANE_DOOR_KEY
from comm.constants import COMM_SERVOS
from components.state_switch import StateSwitch
from components.state_trigger import StateTrigger

top_lane_rollover = StateSwitch(
    toggle=True,
    state_key=LEFT_LANE_DOOR_KEY
)

left_launcher_door = StateTrigger(
    target_id=51,
    comm_name=COMM_SERVOS,
    state_key=LEFT_LANE_DOOR_KEY
)


def init_left_launcher(game):
    game.register_message_handler(16, top_lane_rollover.handle_message)
    game.register_state_handler(left_launcher_door.handle_state)
    game.register_cleanup_handler(left_launcher_door.untrigger_component)
