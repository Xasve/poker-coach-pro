import cv2
import numpy as np
import os

class CardRecognizer:
    """Reconocedor simple de cartas"""
    
    def __init__(self, template_dir="data/card_templates"):
        self.template_dir = template_dir
        self.templates = {}
        
    def load_templates(self):
        """Cargar plantillas si existen"""
        if os.path.exists(self.template_dir):
            print(f"Directorio de plantillas encontrado: {self.template_dir}")
            return True
        else:
            print(f"Directorio no encontrado: {self.template_dir}")
            return False
    
    def recognize_cards(self, image, card_regions):
        """Reconocer cartas (simulación)"""
        if not card_regions:
            return []
        
        # Por ahora devolver cartas de prueba
        return ["A♠", "K♥"]
