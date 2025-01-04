import pygame
import random

# Inicialización
pygame.init()
win_width, win_height = 1000, 800
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Simulación de partículas")
clock = pygame.time.Clock()

# Colores y partículas
particles = []
particle_count = 1000


for _ in range(particle_count):
    x = random.randint(0, win_width - 20)
    y = random.randint(0, win_height - 20)
    color = [random.randint(0, 255) for _ in range(3)]
    speed = [random.choice([-1, 1]) * random.randint(5, 10), random.choice([-1, 1]) * random.randint(5, 10)]
    particles.append({"pos": [x, y], "color": color, "speed": speed})

print (particles)
# Bucle principal
running = True
while running:
    win.fill((0, 0, 0))  # Fondo negro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de partículas
    for particle in particles:
        x, y = particle["pos"]
        xspeed, yspeed = particle["speed"]

        # Detectar colisiones con los bordes
        if x <= 0 or x + 20 >= win_width:
            xspeed = -xspeed
        if y <= 0 or y + 20 >= win_height:
            yspeed = -yspeed

        # Actualizar posición y velocidad
        particle["speed"] = [xspeed, yspeed]
        particle["pos"] = [x + xspeed, y + yspeed]
        # Dibujar la partícula
        pygame.draw.ellipse(win, particle["color"], (x, y, 5, 5))

    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()
