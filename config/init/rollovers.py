from components.simple_state_indicator import SimpleStateIndicator

# flash on pattern
ballSaveIndicator1 = SimpleStateIndicator(
    light_group_id=21,
    pattern_id=6,
    variant_id=1,
    pattern_option=3,
    indicator_key="ball_save_indicator_1",
    state_callback=lambda gameState: gameState.is_ball_save_active()
)
ballSaveIndicator2 = SimpleStateIndicator(
    light_group_id=22,
    pattern_id=6,
    variant_id=1,
    pattern_option=3,
    indiator_key="ball_save_indicator_2",
    state_callback=lambda gameState: gameState.is_ball_save_active()
)


def init_rollovers(game):
    game.register_state_handler(ballSaveIndicator1.handle_state)
    game.register_state_handler(ballSaveIndicator2.handle_state)

    game.register_cleanup_handler(ballSaveIndicator1.handle_cleanup)
    game.register_cleanup_handler(ballSaveIndicator2.handle_cleanup)
