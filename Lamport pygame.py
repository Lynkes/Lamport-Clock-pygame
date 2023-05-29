import pygame
import random
import threading
import time
from Lamport import LamportClock

# Configurações da simulação
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
PROCESS_COLOR = (0, 0, 255)
MESSAGE_COLOR = (255, 0, 0)
FONT_SIZE = 20
FONT_COLOR = (0, 0, 0)

# Classe para representar um processo
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
        message_timestamp = self.clock.get_time()
        self.clock.increment()
        self.messages.append((receiver_id, message_timestamp))

    def receive_message(self, sender_id, message_timestamp):
        self.clock.update(message_timestamp)
        self.messages.append((sender_id, message_timestamp))

    def run(self):
        while True:
            self.send_message()
            time.sleep(random.uniform(0.5, 2.0))  # Simulate random message exchanges

    def draw(self, surface):
        # Desenha o processo como um círculo
        x, y = self.position
        pygame.draw.circle(surface, PROCESS_COLOR, (x, y), 30)

        # Desenha o relógio lógico
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(str(self.clock.get_time()), True, FONT_COLOR)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

        # Desenha as mensagens
        for message in self.messages:
            receiver_id, message_timestamp = message
            pygame.draw.line(surface, MESSAGE_COLOR, (x, y), processes[receiver_id].position, 2)


# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Relógios de Lamport")
clock = pygame.time.Clock()

# Número de processos na simulação
num_processes = 3

# Criação dos processos
processes = []
for i in range(num_processes):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    process_clock = LamportClock()
    process = Process(i, num_processes, process_clock, (x, y))
    processes.append(process)

# Inicialização e execução dos processos
for process in processes:
    process.start()

# Loop principal da simulação
running = True
while running:
    # Limpa a tela
    screen.fill(BACKGROUND_COLOR)

    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha os processos
    for process in processes:
        process.draw(screen)

    # Atualiza a tela
    pygame.display.flip()

    # Controla a taxa de quadros por segundo
    clock.tick(30)

# Encerra o Pygame
pygame.quit()
