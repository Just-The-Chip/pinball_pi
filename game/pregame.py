class PreGame:

    def __init__(self, start_button_id, comm_handler, screen) -> None:
        self.comm_handler = comm_handler
        self.start_button_id = start_button_id
        self.screen = screen
        self.game_in_progress = False
        self.log_messages = False

    def resume(self):
        self.game_in_progress = False
        self.screen.set_mode(0)

    def loop(self):
        while not self.game_in_progress:
            self.handle_incoming_messages()
            self.update_screen()

    # 00000000  0000 0000
    # ---id---  ---msg---
    def handle_incoming_messages(self):
        messages = self.comm_handler.read_all()

        # self.printMsg(f"message count: {len(messages)}")
        for id_message in messages:
            int_message = int.from_bytes(id_message, byteorder="big")
            id = (int_message >> 8)

            self.printMsg(f"MESSAGE ID: {str(id)}")

            if id == self.start_button_id:
                self.printMsg("GAME STARTED!!!!!!!!!", True)
                self.game_in_progress = True

            else:
                idString = str(id)
                self.printMsg(f"component id not found: {idString}", (len(idString) > 3))

    def update_screen(self):
        self.screen.set_display_text("<(^ ^<) START GAME!!! (>^ ^)>")
        self.screen.update()

    def printMsg(self, message, force=False):
        if self.log_messages or force:
            print(message)
