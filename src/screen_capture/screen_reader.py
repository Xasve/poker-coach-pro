"""
Archivo: screen_reader.py
Ruta: src/screen_capture/screen_reader.py
Lector principal de pantalla para análisis de mesa de poker
"""

from .stealth_capture import StealthScreenCapture, AdaptiveRegionCapture
from typing import Optional, Dict, List
import cv2
import numpy as np
from PIL import Image

class ScreenReader:
    """Lector principal de pantalla para análisis de poker"""
    
    def __init__(self, platform: str = "ggpoker"):
        self.platform = platform
        self.capture_system = StealthScreenCapture(platform=platform)
        self.region_capture = AdaptiveRegionCapture(platform=platform)
        
        # Cache de capturas
        self.last_screenshot = None
        self.last_capture_time = 0
        
    def read_table_state(self) -> Dict:
        """
        Leer estado completo de la mesa de poker
        
        Returns:
            Dict con estado del juego
        """
        try:
            # 1. Capturar pantalla completa
            screenshot = self.capture_system.capture()
            if not screenshot:
                return self._get_empty_state()
            
            self.last_screenshot = screenshot
            self.last_capture_time = time.time()
            
            # 2. Detectar elementos de la mesa
            table_state = {
                'screenshot': screenshot,
                'timestamp': time.time(),
                'platform': self.platform,
                'hero_cards': self._detect_hero_cards(screenshot),
                'board_cards': self._detect_board_cards(screenshot),
                'pot_size': self._detect_pot_size(screenshot),
                'hero_stack': self._detect_hero_stack(screenshot),
                'action_required': self._detect_action_required(screenshot),
                'table_detected': True
            }
            
            return table_state
            
        except Exception as e:
            print(f"[Screen Reader] Error: {e}")
            return self._get_empty_state()
    
    def _detect_hero_cards(self, screenshot: Image.Image) -> List[str]:
        """Detectar cartas del héroe"""
        # TODO: Implementar detección real de cartas
        # Por ahora retornar lista vacía
        return []
    
    def _detect_board_cards(self, screenshot: Image.Image) -> List[str]:
        """Detectar cartas comunitarias"""
        # TODO: Implementar detección real
        return []
    
    def _detect_pot_size(self, screenshot: Image.Image) -> float:
        """Detectar tamaño del pot"""
        # TODO: Implementar OCR para leer pot
        return 0.0
    
    def _detect_hero_stack(self, screenshot: Image.Image) -> float:
        """Detectar stack del héroe"""
        # TODO: Implementar OCR para leer stack
        return 100.0
    
    def _detect_action_required(self, screenshot: Image.Image) -> bool:
        """Detectar si hay acción requerida"""
        # TODO: Implementar detección de botones de acción
        return False
    
    def _get_empty_state(self) -> Dict:
        """Obtener estado vacío"""
        return {
            'screenshot': None,
            'timestamp': time.time(),
            'platform': self.platform,
            'hero_cards': [],
            'board_cards': [],
            'pot_size': 0.0,
            'hero_stack': 0.0,
            'action_required': False,
            'table_detected': False
        }