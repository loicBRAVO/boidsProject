import pygame
import numpy as np

class Letter:
    def __init__(self, char, x, y, size):
        self.char = char
        self.position = np.array([x, y])
        self.size = size
        self.points = self.generate_points()

    def lerp(self, start, end, t):
        """Interpolation linéaire entre start et end"""
        return start + (end - start) * t

    def generate_points(self):
        # Example for letter "A"
        if self.char == "A":
            base_points = [
                [-0.5, 1],     # Base gauche
                [-0.4, 0.8],   # Point intermédiaire gauche 1
                [-0.3, 0.6],   # Point intermédiaire gauche 2
                [-0.2, 0.4],   # Point intermédiaire gauche 3
                [-0.1, 0.2],   # Point intermédiaire gauche 4
                [0, -1],       # Sommet
                [0.1, 0.2],    # Point intermédiaire droit 4
                [0.2, 0.4],    # Point intermédiaire droit 3
                [0.3, 0.6],    # Point intermédiaire droit 2
                [0.4, 0.8],    # Point intermédiaire droit 1
                [0.5, 1],      # Base droite
                # Points pour la barre horizontale
                [-0.25, 0],    # Barre gauche
                [-0.15, 0],    # Point intermédiaire barre 1
                [0, 0],        # Point central barre
                [0.15, 0],     # Point intermédiaire barre 2
                [0.25, 0],     # Barre droite
            ]
            return [np.array([x * self.size + self.position[0],
                            y * self.size + self.position[1]]) for x, y in base_points]
        # Points for letter "O"
        if self.char == "O":
            # Création d'un O typographique avec épaisseur
            outer_points = []
            inner_points = []
            num_points = 32  # Plus de points pour plus de précision
            
            # Paramètres de la forme
            outer_width = 0.5
            outer_height = 1.0
            inner_width = 0.25
            inner_height = 0.7
            
            # Génération des points externes et internes
            for i in range(num_points):
                angle = 2 * np.pi * i / num_points
                # Points du contour externe (plus large)
                x_out = outer_width * np.cos(angle)
                y_out = outer_height * np.sin(angle)
                outer_points.append([x_out, y_out])
                
                # Points du contour interne (plus étroit)
                x_in = inner_width * np.cos(angle)
                y_in = inner_height * np.sin(angle)
                inner_points.append([x_in, y_in])
            
            # Fermer les contours
            outer_points.append(outer_points[0])
            inner_points.append(inner_points[0])
            
            # Combiner les points
            all_points = outer_points + inner_points[::-1]  # Inverse les points internes
            
            return [np.array([x * self.size + self.position[0],
                            y * self.size + self.position[1]]) for x, y in all_points]
        if self.char == "Z":
            width = 0.8
            height = 1.0
            num_points = 5  # Nombre de points par segment
            points = []
            
            # Barre supérieure avec plus de points intermédiaires
            for i in range(num_points):
                t = i / (num_points - 1)
                points.append([-width/2 + width*t, -height/2])
            
            # Diagonale avec plus de points intermédiaires
            for i in range(num_points):
                t = i / (num_points - 1)
                x = width/2 - width*t
                y = -height/2 + height*t
                points.append([x, y])
            
            # Barre inférieure avec plus de points intermédiaires
            for i in range(num_points):
                t = i / (num_points - 1)
                points.append([-width/2 + width*t, height/2])
            
            return [np.array([x * self.size + self.position[0],
                            y * self.size + self.position[1]]) for x, y in points]
        return []

    def get_closest_point(self, pos):
        min_dist = float('inf')
        closest = self.points[0]
        for point in self.points:
            dist = np.linalg.norm(point - pos)
            if dist < min_dist:
                min_dist = dist
                closest = point
        return closest

    def get_min_distance_to_segments(self, pos):
        min_dist = float('inf')
        closest_point = None
        
        for i in range(len(self.points)-1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            # Calcul du point le plus proche sur le segment
            segment = p2 - p1
            length_sq = np.dot(segment, segment)
            if length_sq == 0:
                continue
                
            t = max(0, min(1, np.dot(pos - p1, segment) / length_sq))
            projection = p1 + t * segment
            
            dist = np.linalg.norm(pos - projection)
            if dist < min_dist:
                min_dist = dist
                closest_point = projection
        
        return min_dist, closest_point

    def draw(self, screen):
        if len(self.points) > 1:
            # Dessiner d'abord une ligne plus épaisse en noir pour l'effet de contour
            for i in range(len(self.points)-1):
                pygame.draw.line(screen, (50, 50, 50),
                               self.points[i].astype(int),
                               self.points[i+1].astype(int), 3)
            
            # Puis une ligne plus fine en blanc par dessus
            for i in range(len(self.points)-1):
                pygame.draw.line(screen, (200, 200, 200),
                               self.points[i].astype(int),
                               self.points[i+1].astype(int), 1)

            # Ajouter des points aux intersections pour plus de détail
            for point in self.points:
                pygame.draw.circle(screen, (200, 200, 200), 
                                 point.astype(int), 2)
