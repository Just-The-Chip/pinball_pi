import serial


class BaseComm:
    def __init__(self, **kwargs) -> None:
        self.port = kwargs.pop("port")
        self.baud_rate = kwargs.pop("baud_rate", 115200)
        self.message_size = kwargs.pop("message_size", 4)
        self.name = kwargs.pop("name", "")
        self.log_messages = False
        self.init_serial()

    def init_serial(self):
        self.serial = serial.Serial(
            self.port, self.baud_rate, timeout=1, write_timeout=1)
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def read_buffer(self):
        messages = []
        lines_read = 0

        if self.serial.in_waiting > 0:
            self.printMsg(f"in waiting: {str(self.serial.in_waiting)}")

        while self.serial.in_waiting >= self.message_size:
            self.printMsg(
                f"current waiting: {self.serial.in_waiting}............................")
            line = self.serial.readline()

            if len(line) > self.message_size:
                self.printMsg(f"Line too long: {str(line)}", True)

            # if line doesn't end with EOL character DUMP IT IN THE TRASH!!!!
            if '\\n' in str(line):
                messages.append(line.rstrip())
                lines_read += 1
                self.printMsg(f"lines read: {lines_read}")
            else:
                self.printMsg(f"Bad line: {str(line)}", True)

        return messages

    def write_message(self, message):
        self.serial.write(message)

    def printMsg(self, message, force=False):
        if self.log_messages or force:
            print(f"{self.name} -- {message}")
