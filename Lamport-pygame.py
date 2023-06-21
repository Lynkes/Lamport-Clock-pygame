import pygame
import random
import threading
import time
import math

# Simulation settings
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
PROCESS_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Cores fixas para cada processo
PROCESS_COLOR = (0, 0, 255)
FONT_SIZE = 30
#FONT_COLOR = (0, 0, 0)
FONT_COLOR = []
MAX_MESSAGES = 20  # Número máximo de mensagens no histórico de cada processo

# Class to represent a process
class Process(threading.Thread):
    def __init__(self, process_id, num_processes, clock, position):
        threading.Thread.__init__(self)
        self.process_id = process_id
        self.num_processes = num_processes
        self.clock = clock
        self.position = position
        self.messages = []

    def send_message(self):
        receiver_id = random.randint(0, self.num_processes - 1)
        while receiver_id == self.process_id:  # Avoid sending messages to self
            receiver_id = random.randint(0, self.num_processes - 1)
        message_timestamp = self.clock.get_time()
        self.clock.increment()
        self.clock.update(self.clock.get_time())

        # Limpar as mensagens anteriores antes de enviar uma nova mensagem
        self.messages.clear()

        self.messages.append((receiver_id, message_timestamp))

    def receive_message(self, sender_id, message_timestamp):
        self.clock.update(message_timestamp)
        self.messages.append((sender_id, message_timestamp))
        if len(self.messages) > MAX_MESSAGES:
            self.messages.pop(0)  # Remove oldest message

    def run(self):
        while True:
            self.send_message()
            time.sleep(random.uniform(0.1, 0.2))  # Alteração da velocidade de envio

    def draw(self, surface):
        x, y = self.position
        pygame.draw.circle(surface, PROCESS_COLORS[self.process_id], (x, y), 30)  # Alteração da cor do processo

        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render("" + str(self.clock.get_time()), True, FONT_COLOR[self.process_id])
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

        for i, message in enumerate(self.messages):
            receiver_id, message_timestamp = message
            receiver_position = processes[receiver_id].position
            start_pos = (x + 30 * math.cos(get_angle(x, y, receiver_position[0], receiver_position[1])),
                         y + 30 * math.sin(get_angle(x, y, receiver_position[0], receiver_position[1])))
            end_pos = (receiver_position[0] + 30 * math.cos(get_angle(receiver_position[0], receiver_position[1], x, y)),
                       receiver_position[1] + 30 * math.sin(get_angle(receiver_position[0], receiver_position[1], x, y)))

            color = PROCESS_COLORS[self.process_id]  # Usar a cor do próprio processo
            pygame.draw.line(surface, color, start_pos, end_pos, 3)
            draw_arrow(surface, color, start_pos, end_pos)

def get_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

def draw_arrow(surface, color, start_pos, end_pos, arrow_size=10, line_width=3):
    pygame.draw.line(surface, color, start_pos, end_pos, line_width)

    angle = get_angle(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    arrowhead_1 = (end_pos[0] - arrow_size * math.cos(angle + math.pi / 6),
                   end_pos[1] - arrow_size * math.sin(angle + math.pi / 6))
    arrowhead_2 = (end_pos[0] - arrow_size * math.cos(angle - math.pi / 6),
                   end_pos[1] - arrow_size * math.sin(angle - math.pi / 6))

    pygame.draw.polygon(surface, color, (end_pos, arrowhead_1, arrowhead_2))

class LamportClock:
    def __init__(self):
        self.clock = 0

    def increment(self):
        self.clock += 1

    def update(self, received_time):
        self.clock = max(self.clock, received_time)

    def get_time(self):
        return self.clock

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Relógios de Lamport")
clock = pygame.time.Clock()

num_processes = 32

i=0
while i<num_processes:
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)
    PROCESS_COLORS.append([r,g,b])
    FONT_COLOR.append([255-r,255-g,255-b])
    i+=1
    #PROCESS_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] 

triangle_side = min(WIDTH, HEIGHT) * 0.4
triangle_center = (WIDTH // 2, HEIGHT // 2)
vertex_angle = 2 * math.pi / num_processes

processes = []
for i in range(num_processes):
    x = int(triangle_center[0] + triangle_side * math.cos(i * vertex_angle))
    y = int(triangle_center[1] + triangle_side * math.sin(i * vertex_angle))
    process_clock = LamportClock()
    process = Process(i, num_processes, process_clock, (x, y))
    processes.append(process)
    process.start()

running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for process in processes:
        process.draw(screen)

    pygame.display.flip()
    clock.tick(500)

pygame.quit()
