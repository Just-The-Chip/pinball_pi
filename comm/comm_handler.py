class CommHandler:

    comms = {}
    write_queue = {}

    def __init__(self) -> None:
        pass

    def register_comm(self, comm_name, comm):
        self.comms[comm_name] = comm
        self.write_queue[comm_name] = []

    def read_all(self):
        messages = []
        for comm in self.comms.values():
            messages.extend(comm.read_buffer())

        return messages

    def write_all_queued(self):
        for comm_name in self.write_queue:
            self.write_queued(comm_name)

    def write_queued(self, comm_name):
        comm = self.comms[comm_name]
        queue = self.write_queue[comm_name]

        while len(queue) > 0:
            message = queue.pop(0)
            print(f"WRITING MESSAGE ({comm_name}):")
            print(message)
            comm.write_message(message)

    def queue_message(self, comm_name, message):
        self.write_queue[comm_name].append(message)
