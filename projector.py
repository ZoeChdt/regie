"""
projector.py - Gestion d'un projecteur individuel utilisant config.py
"""
from config import PROJECTOR_CONFIG

class Projector:
    def __init__(self, projector_id):
        self.id = projector_id
        self.color = PROJECTOR_CONFIG['default_color']
        self.base_color = PROJECTOR_CONFIG['default_color']
        self.is_on = False
        self.intensity = PROJECTOR_CONFIG['default_intensity']
        self.rect = None
        self.max_intensity = PROJECTOR_CONFIG['max_intensity']
        self.min_intensity = PROJECTOR_CONFIG['min_intensity']
        
    def set_color(self, color):
        """Définir la couleur du projecteur"""
        self.color = color
        self.base_color = color
        
    def set_intensity(self, intensity):
        """Définir l'intensité avec limites configurées"""
        self.intensity = max(self.min_intensity, 
                           min(self.max_intensity, intensity))
        
    def turn_on(self):
        """Allumer le projecteur"""
        self.is_on = True
        
    def turn_off(self):
        """Éteindre le projecteur"""
        self.is_on = False
        
    def toggle(self):
        """Basculer l'état on/off"""
        self.is_on = not self.is_on
        
    def get_dimmed_color(self):
        """Calculer la couleur avec l'intensité appliquée"""
        if self.intensity == self.min_intensity or not self.is_on:
            return "black"
        
        hex_color = self.color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        intensity_factor = self.intensity / self.max_intensity
        r = int(r * intensity_factor)
        g = int(g * intensity_factor)
        b = int(b * intensity_factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def get_state(self):
        """Retourner l'état complet du projecteur"""
        return {
            'color': self.base_color,
            'is_on': self.is_on,
            'intensity': self.intensity
        }
    
    def set_state(self, state):
        """Appliquer un état complet au projecteur"""
        self.color = state['color']
        self.base_color = state['color']
        self.is_on = state['is_on']
        self.set_intensity(state['intensity'])
    
    def __str__(self):
        status = "ON" if self.is_on else "OFF"
        return f"Projecteur {self.id+1}: {status}, Couleur: {self.base_color}, Intensité: {self.intensity}%"