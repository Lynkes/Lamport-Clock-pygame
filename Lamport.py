import random
import threading
import time

class LamportClock:
    def __init__(self):
        self.clock = 0

    def increment(self):
        self.clock += 1

    def update(self, received_time):
        self.clock = max(self.clock, received_time) + 1

    def get_time(self):
        return self.clock


class Process(threading.Thread):
    def __init__(self, process_id, num_processes):
        threading.Thread.__init__(self)
        self.process_id = process_id
        self.num_processes = num_processes
        self.clock = LamportClock()

    def send_message(self):
        receiver_id = random.randint(0, self.num_processes - 1)
        message_timestamp = self.clock.get_time()
        print(f"Process {self.process_id}: Sending message to process {receiver_id} with timestamp {message_timestamp}")
        processes[receiver_id].receive_message(message_timestamp)

    def receive_message(self, message_timestamp):
        self.clock.update(message_timestamp)
        print(f"Process {self.process_id}: Received message with timestamp {message_timestamp}. Updated clock to {self.clock.get_time()}")

    def run(self):
        while True:
            self.clock.increment()
            print(f"Process {self.process_id}: Event occurred. Clock: {self.clock.get_time()}")
            time.sleep(random.uniform(0.5, 2.0))  # Simulate random local events
            self.send_message()
            time.sleep(random.uniform(0.5, 2.0))  # Simulate random message exchanges


# Número de processos no sistema
num_processes = 3

# Criação dos processos
processes = []
for i in range(num_processes):
    process = Process(i, num_processes)
    processes.append(process)

# Inicialização e execução dos processos
for process in processes:
    process.start()

# Aguarda a finalização dos processos
for process in processes:
    process.join()
