import pygame  # Import the Pygame library for creating graphics and games
import random  # Import the random module for generating random numbers
import threading  # Import the threading module for running multiple threads simultaneously
import time  # Import the time module for introducing delays in the program

# Simulation settings
WIDTH = 1024
HEIGHT = 768
BACKGROUND_COLOR = (255, 255, 255)  # White background color for the screen
PROCESS_COLOR = (0, 0, 255)  # Blue color for the processes
MESSAGE_COLOR = (255, 0, 0)  # Red color for the messages
FONT_SIZE = 50
FONT_COLOR = (0, 0, 0)  # Black font color for the text

# Class to represent a process
class Process(threading.Thread):
    def __init__(self, process_id, num_processes, clock, position):
        threading.Thread.__init__(self)
        self.process_id = process_id  # The unique identifier of the process
        self.num_processes = num_processes  # The total number of processes in the simulation
        self.clock = clock  # An instance of LamportClock class for managing logical clocks
        self.position = position  # The position of the process on the screen
        self.messages = []  # A list of messages (tuples) sent and received by the process

    def send_message(self):
        # Choose a random receiver among all processes
        receiver_id = random.randint(0, self.num_processes - 1)
        # Get the current timestamp of the process's clock
        message_timestamp = self.clock.get_time()
        # Increment the process's clock before sending the message
        self.clock.increment()
        # Append the message (receiver_id, message_timestamp) to the list of messages
        self.messages.append((receiver_id, message_timestamp))

    def receive_message(self, sender_id, message_timestamp):
        # Update the process's clock with the timestamp of the received message
        self.clock.update(message_timestamp)
        # Append the message (sender_id, message_timestamp) to the list of messages
        self.messages.append((sender_id, message_timestamp))

    def run(self):
        # The main loop of the thread that sends messages randomly and sleeps for a random time between 0.5 and 2 seconds
        while True:
            self.send_message()
            time.sleep(random.uniform(0.5, 2.0))  # Simulate random message exchanges

    def draw(self, surface):
        # Draw the process as a circle on the screen
        x, y = self.position
        pygame.draw.circle(surface, PROCESS_COLOR, (x, y), 30)

        # Draw the logical clock value of the process as text on the circle
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(str(self.clock.get_time()), True, FONT_COLOR)
        # Center the text inside the circle
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

        # Draw the messages sent and received by the process as lines on the screen
        for message in self.messages:
            receiver_id, message_timestamp = message
            # Draw a line from the current process to the receiver process
            pygame.draw.line(surface, MESSAGE_COLOR, (x, y), processes[receiver_id].position, 2)

class LamportClock:
    def __init__(self):
        self.clock = 0

    def increment(self):
        self.clock += 1

    def update(self, received_time):
        self.clock = max(self.clock, received_time) + 1

    def get_time(self):
        return self.clock

# Initialization of Pygame library and creation of a display window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Relógios de Lamport")  # Set the caption of the window
clock = pygame.time.Clock()  # Create a clock object for controlling the frame rate

# Number of processes in the simulation
num_processes = 3

# Create the processes with random positions and start them as threads
processes = []
for i in range(num_processes):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    process_clock = LamportClock()  # Create a new instance of LamportClock class for each process
    process = Process(i, num_processes, process_clock, (x, y))
    processes.append(process)
    process.start()

# Main loop of the simulation
running = True
while running:
    # Clear the screen with the background color
    screen.fill(BACKGROUND_COLOR)

    # Handle events (only QUIT event is recognized)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the processes and messages on the screen
    for process in processes:
        process.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control the frame rate of the simulation
    clock.tick(60)  # Limit the frame rate to 30 FPS

# Cleanup the resources used by Pygame
pygame.quit() 
