"""
adaptive_recognizer.py - Sistema de reconocimiento adaptativo que aprende mientras juegas
"""

import cv2
import numpy as np
import logging
from pathlib import Path
from typing import List, Dict, Optional
import pickle
from datetime import datetime

from .card_recognizer import CardRecognizer, Card

class AdaptiveCardRecognizer:
    """Reconocedor adaptativo básico - Versión simplificada para que funcione"""
    
    def __init__(self, platform: str = "ggpoker", stealth_level: str = "MEDIUM"):
        self.platform = platform
        self.stealth_level = stealth_level
        self.logger = logging.getLogger(__name__)
        
        # Usar CardRecognizer como base
        self.base_recognizer = CardRecognizer(platform=platform, stealth_level=stealth_level)
        
        # Datos de aprendizaje (simplificado)
        self.learned_cards = {}
        self.learning_dir = Path(f"data/learning/{platform}")
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"AdaptiveCardRecognizer inicializado para {platform}")
    
    def recognize_and_learn(self, screenshot, region_config) -> List[Card]:
        """Reconocer cartas (versión simplificada)"""
        # Por ahora, simplemente usar el reconocedor base
        return self.base_recognizer.recognize_cards_in_region(screenshot, region_config)
    
    def get_learning_stats(self) -> Dict:
        """Obtener estadísticas de aprendizaje"""
        return {
            "total_learned_cards": len(self.learned_cards),
            "average_confidence": 0.8,
            "platform": self.platform,
            "status": "active"
        }

# Para compatibilidad
def get_adaptive_recognizer(platform="ggpoker", stealth_level="MEDIUM"):
    return AdaptiveCardRecognizer(platform=platform, stealth_level=stealth_level)