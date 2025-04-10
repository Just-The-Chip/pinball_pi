class PreGame:

    def __init__(self, start_button_id, comm_handler, screen) -> None:
        self.comm_handler = comm_handler
        self.start_button_id = start_button_id
        self.screen = screen
        self.game_in_progress = False
        self.log_messages = True

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

            print(f"MESSAGE ID: {str(id)}")

            if id == self.start_button_id:
                print("GAME STARTED!!!!!!!!!")
                self.game_in_progress = True

            else:
                self.printMsg(f"component id not found: {str(id)}")

    def update_screen(self):
        self.screen.update()

    def printMsg(self, message):
        if self.log_messages:
            print(message)
