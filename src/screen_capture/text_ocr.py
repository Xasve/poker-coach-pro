"""
text_ocr.py - Reconocimiento de texto (OCR) para montos y texto de poker
"""

import logging
from typing import Optional, Tuple, Dict
import numpy as np

class TextOCR:
    """Clase básica para reconocimiento de texto"""
    
    def __init__(self, platform: str = "ggpoker"):
        self.platform = platform
        self.logger = logging.getLogger(__name__)
        
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)
        
        self.logger.info(f"TextOCR inicializado para {platform}")
    
    def read_pot_amount(self, region_image: np.ndarray) -> Optional[float]:
        """Leer cantidad del pot desde una imagen"""
        self.logger.debug("Leyendo cantidad del pot (implementación básica)")
        
        # Implementación básica - en una versión real usaríamos Tesseract
        # Por ahora retornar valor fijo
        return 0.0
    
    def read_player_stack(self, player_position: int, 
                         region_image: np.ndarray) -> Optional[float]:
        """Leer stack de un jugador"""
        self.logger.debug(f"Leyendo stack del jugador {player_position}")
        
        # Implementación básica
        return 100.0
    
    def read_action_buttons(self, region_image: np.ndarray) -> Dict[str, bool]:
        """Detectar botones de acción disponibles"""
        self.logger.debug("Detectando botones de acción")
        
        # Implementación básica
        return {
            "fold": True,
            "call": True,
            "raise": True,
            "check": False,
            "bet": False
        }
    
    def read_card_text(self, card_image: np.ndarray) -> Optional[str]:
        """Leer texto de una carta (para debugging)"""
        self.logger.debug("Leyendo texto de carta")
        
        # Implementación básica
        return None

# Exportar la clase
__all__ = ['TextOCR']