"""
Configuración específica para PokerStars
"""
import os
from dataclasses import dataclass

@dataclass
class PokerStarsConfig:
    """Configuración para PokerStars"""
    
    # Nombres de archivos de templates
    CARD_TEMPLATES_DIR = os.path.join("data", "card_templates", "pokerstars")
    TABLE_TEMPLATES_DIR = os.path.join("data", "table_templates", "pokerstars")
    
    # Colores característicos de PokerStars
    COLORS = {
        "primary": "#0a5c1f",  # Verde PokerStars
        "secondary": "#ffffff",
        "background": "#1a1a1a",
        "text": "#ffffff"
    }
    
    # Regiones de captura (coordenadas relativas)
    CAPTURE_REGIONS = {
        "hero_cards": {"x1": 0.45, "y1": 0.75, "x2": 0.55, "y2": 0.85},
        "community_cards": {"x1": 0.35, "y1": 0.45, "x2": 0.65, "y2": 0.55},
        "pot_amount": {"x1": 0.48, "y1": 0.35, "x2": 0.52, "y2": 0.40},
        "stack_amount": {"x1": 0.45, "y1": 0.80, "x2": 0.55, "y2": 0.85},
        "to_call_amount": {"x1": 0.48, "y1": 0.60, "x2": 0.52, "y2": 0.65}
    }
    
    # Tamaños esperados
    CARD_SIZE = (70, 95)  # Ancho, alto en píxeles
    TABLE_SIZE = (800, 600)  # Tamaño típico de mesa
    
    # Configuración de reconocimiento
    CONFIDENCE_THRESHOLD = 0.85
    LEARNING_RATE = 0.1
    
    @classmethod
    def setup_directories(cls):
        """Crear directorios necesarios para PokerStars"""
        os.makedirs(cls.CARD_TEMPLATES_DIR, exist_ok=True)
        os.makedirs(cls.TABLE_TEMPLATES_DIR, exist_ok=True)
        
        # Crear subdirectorios para cartas
        for suit in ["hearts", "diamonds", "clubs", "spades"]:
            os.makedirs(os.path.join(cls.CARD_TEMPLATES_DIR, suit), exist_ok=True)
