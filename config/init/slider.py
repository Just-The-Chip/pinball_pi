from components.slider import Slider

slider = Slider(
    base_points_value=10,
    light_group_id=20
)


def init_slider(game):
    game.register_state_handler(slider.handle_state)
    game.register_message_handler(31, slider.handle_message)
