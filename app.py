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
    {"color": (255, 100, 100), "count": 50},
    {"color": (100, 255, 100), "count": 50},
    {"color": (100, 100, 255), "count": 50},
]

# Création des boids par groupe
boids = []
for group_id, group in enumerate(GROUPS):
    for _ in range(group["count"]):
        boids.append(Boid(WIDTH, HEIGHT, group_id, group["color"]))

# Création de trois lettres Z avec un décalage plus petit
letters = [
    Letter("Z", WIDTH/2 - 10, HEIGHT/2 - 10, 250),  # Z arrière
    Letter("Z", WIDTH/2, HEIGHT/2, 250),           # Z milieu
    Letter("Z", WIDTH/2 + 10, HEIGHT/2 + 10, 250),  # Z avant
]

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update - chaque boid choisit une lettre aléatoire
    for boid in boids:
        target_letter = letters[np.random.randint(0, len(letters)) if np.random.random() < 0.01 else boid.current_letter_index]
        boid.update(boids, target_letter)

    # Draw
    screen.fill(BLACK)
    # Dessiner les lettres dans l'ordre (arrière vers avant)
    for letter in letters:
        letter.draw(screen)
    for boid in boids:
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
