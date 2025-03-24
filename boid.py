import numpy as np
import pygame

class Boid:
    def __init__(self, width, height, group_id, color):
        # Position initiale sur un cercle avec un offset aléatoire
        angle = np.random.uniform(0, 2 * np.pi)
        radius = height/4 + np.random.uniform(-20, 20)
        center = np.array([width/2, height/2])
        self.position = center + np.array([np.cos(angle), np.sin(angle)]) * radius
        
        # Vitesse initiale tangente au cercle
        self.velocity = np.array([-np.sin(angle), np.cos(angle)]) * 2
        self.acceleration = np.zeros(2)
        self.max_speed = 2  # Réduit pour plus de précision
        self.max_force = 0.4  # Augmenté pour des virages plus nets
        self.orbit_speed = 0.03 
        self.perception = 50     
        self.separation_distance = 15  # Réduit pour un flux plus serré
        self.group_spacing = 20  # Réduit pour un flux plus serré
        self.size = 6
        self.group_id = group_id
        self.color = color
        self.target_index = 0  # On initialise à 0, sera mis à jour au premier update
        self.path_following_distance = 10  # Distance pour changer de point cible
        self.look_ahead = 3  # Nombre de points à regarder en avance
        self.group_offset = group_id * (360 // 8)  # Distribue les groupes le long du chemin
        self.segment_index = group_id % 3  # Assigne chaque groupe à un segment spécifique
        self.target_index = 0  # On initialisera la vraie valeur dans la première update
        self.initialized = False  # Pour gérer la première initialisation

    def update(self, boids, letter):
        # Initialisation du target_index au premier update
        if not self.initialized and hasattr(letter, 'segments'):
            # Position initiale sur le segment assigné
            segment = letter.segments[self.segment_index]
            self.target_index = np.random.randint(0, len(segment))
            self.position = segment[self.target_index].copy()
            self.initialized = True
            
        # Apply flocking rules
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        path_force = self.circle_behavior(letter)

        # Ajustement des coefficients pour favoriser le suivi de chemin
        self.acceleration += alignment * 0.3
        self.acceleration += cohesion * 0.2
        self.acceleration += separation * 1.0
        self.acceleration += path_force * 3.5

        # Update position
        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

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
            # Utilise group_spacing pour les autres groupes
            separation_threshold = self.group_spacing if boid.group_id != self.group_id else self.separation_distance
            
            if dist < separation_threshold and boid is not self:
                diff = self.position - boid.position
                # Force inversement proportionnelle au carré de la distance
                strength = 1.0 / max(dist * dist, 0.1)
                diff = diff * strength
                
                # Multiplier plus fort entre groupes différents
                multiplier = 3.0 if boid.group_id != self.group_id else 2.0
                steering += diff * multiplier
                total += 1
                
        if total > 0:
            steering = steering / total
            steering = self.limit(steering, self.max_force * 2.0)
        return steering

    def seek_letter(self, letter):
        target = letter.get_closest_point(self.position)
        desired = target - self.position
        desired = desired / np.linalg.norm(desired) * self.max_speed
        steering = desired - self.velocity
        return self.limit(steering, self.max_force)

    def avoid_segments(self, letter):
        dist, closest_point = letter.get_min_distance_to_segments(self.position)
        threshold = 20  # Distance à partir de laquelle la répulsion s'applique
        
        if dist < threshold and closest_point is not None:
            # Direction opposée au segment le plus proche
            direction = self.position - closest_point
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            
            # Force plus importante quand on est proche
            strength = (1 - (dist / threshold)) * self.max_force * 3
            return direction * strength
        
        return np.zeros(2)

    def circle_behavior(self, letter):
        if not hasattr(letter, 'segments') or not self.initialized:
            return np.zeros(2)

        # Les points du segment sont déjà transformés en coordonnées écran
        segment_points = letter.segments[self.segment_index]
        
        # Vérification de sécurité
        if len(segment_points) == 0:
            return np.zeros(2)
            
        # Point actuel et prochain point
        current_index = self.target_index % len(segment_points)
        next_index = (current_index + 1) % len(segment_points)
        
        current_target = segment_points[current_index]
        next_target = segment_points[next_index]
        
        # Distance au point actuel
        dist_to_target = np.linalg.norm(current_target - self.position)

        # Vecteur vers le prochain point pour anticiper la direction
        path_direction = next_target - current_target
        if np.linalg.norm(path_direction) > 0:
            path_direction = path_direction / np.linalg.norm(path_direction)

        # Force principale vers le point actuel
        desired = current_target - self.position
        if np.linalg.norm(desired) > 0:
            desired = desired / np.linalg.norm(desired) * self.max_speed

        # Ajout d'une composante d'anticipation
        steering = desired + path_direction * self.max_speed * 0.5

        # Changement de point cible
        if dist_to_target < self.path_following_distance:
            self.target_index = next_index

        return self.limit(steering, self.max_force)

    def limit(self, vector, max_magnitude):
        mag = np.linalg.norm(vector)
        if mag > max_magnitude:
            vector = vector / mag * max_magnitude
        return vector

    def draw(self, screen):
        # Dessine un triangle orienté dans la direction du mouvement
        direction = self.velocity / np.linalg.norm(self.velocity) if np.linalg.norm(self.velocity) > 0 else np.array([1, 0])
        
        # Calcul des points du triangle
        angle = np.pi * 2/3
        p1 = self.position + direction * self.size
        p2 = self.position + np.array([np.cos(angle) * direction[0] - np.sin(angle) * direction[1],
                                     np.sin(angle) * direction[0] + np.cos(angle) * direction[1]]) * self.size
        p3 = self.position + np.array([np.cos(-angle) * direction[0] - np.sin(-angle) * direction[1],
                                     np.sin(-angle) * direction[0] + np.cos(-angle) * direction[1]]) * self.size
        
        pygame.draw.polygon(screen, self.color, [p1, p2, p3])
