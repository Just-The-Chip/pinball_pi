GAME_OVER_STEP = "game_over"
SCORE_CHECK_STEP = "check_high_score"
NAME_INPUT_STEP = "await_name_input"
EASTER_EGG_STEP = "easter_egg_check"
SCORE_SAVE_STEP = "score_save"

LEFT_FLIPPER = "left_flipper"
RIGHT_FLIPPER = "right_flipper"
START_BUTTON = "start_button"

GAME_OVER_DISPLAY_TIME_MS = 5000
EASTER_EGG_DISPLAY_TIME_MS = 5000


class PostGame:

    def __init__(self, **kwargs) -> None:
        self.comm_handler = kwargs.pop("comm_handler")
        self.screen = kwargs.pop("screen")

        self.input_buttons = {
            kwargs.pop("left_flipper_id"): LEFT_FLIPPER,
            kwargs.pop("right_flipper_id"): RIGHT_FLIPPER,
            kwargs.pop("start_button_id"): START_BUTTON,
        }

        self.postgame_in_progress = False
        self.current_step = GAME_OVER_STEP
        self.button_queue = []
        self.current_character_index = 0
        self.name_position_index = 0
        self.entered_name = []

        self.log_messages = True

    def start(self, gameState):
        self.postgame_in_progress = True
        self.gameState = gameState

        self.current_step = GAME_OVER_STEP
        self.button_queue = []
        self.current_character_index = 0
        self.name_position_index = 0
        self.entered_name = []

        self.screen.set_mode(0)
        self.screen.set_scroll_speed(1)

    def loop(self):
        while self.postgame_in_progress:
            if self.current_step == GAME_OVER_STEP:
                self.game_over_loop()
            elif self.current_step == SCORE_CHECK_STEP:
                self.check_high_score()
            elif self.current_step == NAME_INPUT_STEP:
                self.name_input_loop()
            elif self.current_step == EASTER_EGG_STEP:
                self.easter_egg_loop()
            elif self.current_step == SCORE_SAVE_STEP:
                self.save_score()
            else:
                self.postgame_in_progress = False

    def game_over_loop(self):
        # display "game over" message and then display score
        # move onto check high score step after display time
        pass

    def check_high_score(self):
        # compare score to lowest high score
        # move to name step if score is sufficient, otherwise end postgame
        pass

    def name_input_loop(self):
        # await input from flippers/start button to enter name
        # once three characters have been entered, move to easter egg step
        character_set = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        for button in self.button_queue:
            # Note to self: modulo works different in python because PYTHON JUST HAS TO BE SO SPECIAL
            # whatever, I guess it just so happens to be convenient here
            # https://www.geeksforgeeks.org/python/how-to-perform-modulo-with-negative-values-in-python/
            if button == LEFT_FLIPPER:
                self.current_character_index = (self.current_character_index - 1) % len(character_set)
            elif button == RIGHT_FLIPPER:
                self.current_character_index = (self.current_character_index + 1) % len(character_set)
            elif button == START_BUTTON:
                # select current character
                # display_name[self.name_position_index] = character_set[self.current_character_index]
                self.name_position_index += 1
                self.current_character_index = 0

            if self.name_position_index >= 3:
                self.button_queue = []
                self.current_step = EASTER_EGG_STEP
                return

            self.entered_name[self.name_position_index] = character_set[self.current_character_index]

        self.screen.set_name_data(self.name_position_index, self.entered_name)
        self.screen.update()

    def easter_egg_loop(self):
        # check for silly names
        # if name is sufficiently silly, display a silly message
        # then move to score save step
        pass

    def save_score(self):
        pass

    # 00000000  0000 0000
    # ---id---  ---msg---
    def handle_incoming_messages(self):
        messages = self.comm_handler.read_all()

        # self.print_msg(f"message count: {len(messages)}")
        for id_message in messages:
            int_message = int.from_bytes(id_message, byteorder="big")
            id = (int_message >> 8)

            self.print_msg(f"MESSAGE ID: {str(id)}")

            button_name = self.input_buttons.get(id, None)
            if button_name:
                self.button_queue.append(button_name)
                self.print_msg(f"Button pressed: {button_name}")
            else:
                self.print_msg(f"Unknown button ID: {id}", (len(str(id)) > 3))

    def print_msg(self, message, force=False):
        if self.log_messages or force:
            print(message)
