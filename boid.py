import numpy as np
import pygame

class Boid:
    def __init__(self, width, height, group_id, color):
        angle = np.random.uniform(0, 2 * np.pi)
        radius = height/4 + np.random.uniform(-20, 20)
        center = np.array([width/2, height/2])
        self.position = center + np.array([np.cos(angle), np.sin(angle)]) * radius
        self.velocity = np.random.randn(2) * 2
        self.acceleration = np.zeros(2)
        self.max_speed = 3.5        # Réduit légèrement
        self.max_force = 0.15       # Augmenté pour plus de réactivité
        self.perception = 50        # Réduit pour plus de cohésion locale
        self.size = 4
        self.group_id = group_id
        self.color = color
        self.current_letter_index = np.random.randint(0, 3)

    def update(self, boids, letter):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        target_force = self.seek_target(letter)

        self.acceleration += alignment * 1.2       # Réduit
        self.acceleration += cohesion * 1.2        # Réduit
        self.acceleration += separation * 2      # Réduit
        self.acceleration += target_force * 2    # Augmenté

        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

    def seek_target(self, letter):
        if len(letter.points) == 0:
            return np.zeros(2)
            
        target = letter.get_closest_point(self.position)
        desired = target - self.position
        if np.linalg.norm(desired) > 0:
            desired = desired / np.linalg.norm(desired) * self.max_speed
        steering = desired - self.velocity
        return self.limit(steering, self.max_force)

    def align(self, boids):
        steering = np.zeros(2)
        total = 0
        for boid in boids:
            if boid.group_id != self.group_id:
                continue
            dist = np.linalg.norm(boid.position - self.position)
            if dist < self.perception and boid is not self:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering = steering / total
            steering = self.limit(steering, self.max_force)
        return steering

    def cohesion(self, boids):
        steering = np.zeros(2)
        total = 0
        for boid in boids:
            if boid.group_id != self.group_id:
                continue
            dist = np.linalg.norm(boid.position - self.position)
            if dist < self.perception and boid is not self:
                steering += boid.position
                total += 1
        if total > 0:
            steering = steering / total - self.position
            steering = self.limit(steering, self.max_force)
        return steering

    def separation(self, boids):
        steering = np.zeros(2)
        total = 0
        for boid in boids:
            dist = np.linalg.norm(boid.position - self.position)
            separation_threshold = self.perception / 2
            
            if dist < separation_threshold and boid is not self:
                diff = self.position - boid.position
                strength = 1.0 / max(dist * dist, 0.1)
                diff = diff * strength
                steering += diff
                total += 1
                
        if total > 0:
            steering = steering / total
            steering = self.limit(steering, self.max_force)
        return steering

    def limit(self, vector, max_magnitude):
        mag = np.linalg.norm(vector)
        if mag > max_magnitude:
            vector = vector / mag * max_magnitude
        return vector

    def draw(self, screen):
        direction = self.velocity / np.linalg.norm(self.velocity) if np.linalg.norm(self.velocity) > 0 else np.array([1, 0])
        
        angle = np.pi * 2/3
        p1 = self.position + direction * self.size
        p2 = self.position + np.array([np.cos(angle) * direction[0] - np.sin(angle) * direction[1],
                                     np.sin(angle) * direction[0] + np.cos(angle) * direction[1]]) * self.size
        p3 = self.position + np.array([np.cos(-angle) * direction[0] - np.sin(-angle) * direction[1],
                                     np.sin(-angle) * direction[0] + np.cos(-angle) * direction[1]]) * self.size
        
        pygame.draw.polygon(screen, self.color, [p1, p2, p3])
