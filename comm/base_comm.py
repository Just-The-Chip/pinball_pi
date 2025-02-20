import serial


class BaseComm:
    def __init__(self, **kwargs) -> None:
        self.port = kwargs.pop("port")
        self.baud_rate = kwargs.pop("baud_rate", 115200)
        self.message_size = kwargs.pop("message_size", 4)
        self.log_messages = True
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
                self.printMsg(f"Line too long: {str(line)}")

            # if line doesn't end with EOL character DUMP IT IN THE TRASH!!!!
            if '\\n' in str(line):
                messages.append(line.rstrip())
                lines_read += 1
                self.printMsg(f"lines read: {lines_read}")
            else:
                self.printMsg(f"Bad line: {str(line)}")

        return messages

    def write_message(self, message):
        # this might be wrong but we haven't hooked up a component that requires it yets
        self.serial.write(message)

    def printMsg(self, message):
        if self.log_messages:
            print(message)
