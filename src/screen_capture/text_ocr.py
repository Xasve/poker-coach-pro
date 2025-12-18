"""
text_ocr.py - Reconocimiento de texto (OCR) para montos y texto de poker
Versión básica inicial - Implementación completa pendiente
"""

import logging
from typing import Optional, Tuple, Dict

class TextOCR:
    """Clase básica para reconocimiento de texto"""
    
    def __init__(self, platform: str = "ggpoker"):
        self.platform = platform
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"TextOCR inicializado para {platform}")
    
    def read_pot_amount(self, region_image) -> Optional[float]:
        """Leer cantidad del pot desde una imagen"""
        self.logger.debug("Leyendo cantidad del pot (implementación básica)")
        return 0.0  # Valor por defecto
    
    def read_player_stack(self, player_position: int) -> Optional[float]:
        """Leer stack de un jugador"""
        self.logger.debug(f"Leyendo stack del jugador {player_position} (básico)")
        return 100.0  # Valor por defecto
    
    def read_action_buttons(self) -> Dict[str, bool]:
        """Detectar botones de acción disponibles"""
        self.logger.debug("Detectando botones de acción (básico)")
        return {
            "fold": True,
            "call": True,
            "raise": True,
            "check": False,
            "bet": False
        }

# Exportar la clase
__all__ = ['TextOCR']