import pygame
import numpy as np
from boid import Boid
from letter import Letter

# Initialize Pygame
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Typography")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Définition des groupes avec moins de boids par groupe
GROUPS = [
    {"color": (255, 255, 255), "count": 40},
    {"color": (255, 255, 255), "count": 40},
    {"color": (255, 255, 255), "count": 40},
]

# Création des boids par groupe
boids = []
for group_id, group in enumerate(GROUPS):
    for _ in range(group["count"]):
        boids.append(Boid(WIDTH, HEIGHT, group_id, group["color"]))

current_letter = Letter("Z", WIDTH/2, HEIGHT/2, 100)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    for boid in boids:
        boid.update(boids, current_letter)

    # Draw
    screen.fill(BLACK)
    current_letter.draw(screen)
    for boid in boids:
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
