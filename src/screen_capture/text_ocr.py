"""
text_ocr.py - OCR básico para leer texto (versión simplificada)
"""

import logging
from typing import Optional, Dict
import numpy as np

class TextOCR:
    """OCR básico - Versión simplificada"""
    
    def __init__(self, platform: str = "ggpoker"):
        self.platform = platform
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"TextOCR inicializado para {platform}")
    
    def read_pot_amount(self, region_image) -> float:
        """Leer cantidad del pot"""
        self.logger.debug("Leyendo pot amount (implementación básica)")
        return 0.0  # Valor por defecto
    
    def read_player_stack(self, region_image) -> float:
        """Leer stack del jugador"""
        self.logger.debug("Leyendo player stack (básico)")
        return 100.0  # Valor por defecto
    
    def read_action_buttons(self, region_image) -> Dict[str, bool]:
        """Detectar botones de acción"""
        self.logger.debug("Detectando botones de acción (básico)")
        return {
            "fold": True,
            "call": True,
            "raise": True,
            "check": False,
            "bet": False
        }