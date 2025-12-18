"""
Archivo: table_detector.py
Ruta: src/screen_capture/table_detector.py
Detección de elementos de mesa de poker: posiciones, botones, etc.
"""

import cv2
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json

@dataclass
class TableElement:
    """Elemento detectado en la mesa"""
    element_type: str  # 'button', 'dealer', 'player', 'pot', 'cards'
    position: Tuple[int, int]  # (x, y)
    confidence: float
    size: Tuple[int, int]  # (width, height)
    color: Tuple[int, int, int]  # (B, G, R)

class TablePosition(Enum):
    """Posiciones en la mesa de poker"""
    UTG = "UTG"      # Under The Gun
    MP = "MP"        # Middle Position
    CO = "CO"        # Cutoff
    BTN = "BTN"      # Button
    SB = "SB"        # Small Blind
    BB = "BB"        # Big Blind

class TableDetector:
    """
    Detector de elementos de mesa de poker
    Identifica posiciones, botones, stacks, etc.
    """
    
    def __init__(self, platform: str = "ggpoker"):
        """
        Inicializar detector de mesa
        
        Args:
            platform: "ggpoker" o "pokerstars"
        """
        self.platform = platform.lower()
        self.config = self._load_platform_config()
        
        # Colores característicos por plataforma
        self.platform_colors = {
            "ggpoker": {
                "button_color": (0, 215, 255),  # Dorado GG (BGR)
                "pot_color": (0, 215, 255),     # Dorado para pot
                "player_highlight": (255, 0, 0) # Azul para jugador activo
            },
            "pokerstars": {
                "button_color": (0, 153, 255),  # Naranja PokerStars
                "pot_color": (0, 153, 255),     # Naranja para pot
                "player_highlight": (255, 0, 0) # Azul para jugador activo
            }
        }
        
        print(f"[Table Detector] Inicializado para {self.platform.upper()}")
    
    def _load_platform_config(self) -> Dict:
        """Cargar configuración específica de plataforma"""
        
        configs = {
            "ggpoker": {
                "table_color_range": {
                    "lower": [50, 100, 50],    # Verde oscuro
                    "upper": [100, 255, 150]   # Verde claro
                },
                "button_size": 20,  # Tamaño del botón en píxeles
                "player_positions": self._get_6max_positions(),
                "detection_threshold": 0.7
            },
            "pokerstars": {
                "table_color_range": {
                    "lower": [0, 50, 0],       # Verde muy oscuro
                    "upper": [100, 255, 100]   # Verde
                },
                "button_size": 18,
                "player_positions": self._get_6max_positions(),
                "detection_threshold": 0.7
            }
        }
        
        return configs.get(self.platform, configs["ggpoker"])
    
    def _get_6max_positions(self) -> Dict:
        """Obtener posiciones teóricas para mesa 6-max"""
        # Coordenadas relativas (0-1) para una mesa circular
        return {
            "UTG": {"x": 0.25, "y": 0.15},
            "MP": {"x": 0.40, "y": 0.10},
            "CO": {"x": 0.75, "y": 0.15},
            "BTN": {"x": 0.85, "y": 0.50},
            "SB": {"x": 0.75, "y": 0.85},
            "BB": {"x": 0.25, "y": 0.85}
        }
    
    def detect_table_elements(self, image: Image.Image) -> Dict:
        """
        Detectar todos los elementos de la mesa
        
        Args:
            image: PIL Image de la mesa
            
        Returns:
            Dict con elementos detectados
        """
        try:
            # Convertir a OpenCV
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Detectar diferentes elementos
            elements = {
                'button': self._detect_dealer_button(cv_image),
                'player_positions': self._detect_player_positions(cv_image),
                'pot_area': self._detect_pot_area(cv_image),
                'cards_areas': self._detect_cards_areas(cv_image),
                'action_buttons': self._detect_action_buttons(cv_image),
                'table_detected': True
            }
            
            # Determinar posición del héroe
            elements['hero_position'] = self._determine_hero_position(elements['player_positions'])
            
            return elements
            
        except Exception as e:
            print(f"[Table Detector] Error: {e}")
            return {'table_detected': False, 'error': str(e)}
    
    def _detect_dealer_button(self, cv_image: np.ndarray) -> Optional[TableElement]:
        """Detectar botón de dealer"""
        
        try:
            # Obtener color del botón para esta plataforma
            button_color = self.platform_colors.get(self.platform, {}).get("button_color", (0, 215, 255))
            
            # Convertir a HSV para mejor detección de color
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Crear rango de color para el botón
            hsv_color = cv2.cvtColor(np.uint8([[button_color]]), cv2.COLOR_BGR2HSV)[0][0]
            
            lower_color = np.array([hsv_color[0] - 10, 100, 100])
            upper_color = np.array([hsv_color[0] + 10, 255, 255])
            
            # Crear máscara
            mask = cv2.inRange(hsv, lower_color, upper_color)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Tomar el contorno más grande
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                
                # Filtrar por tamaño
                button_size = self.config.get("button_size", 20)
                min_area = 3.14 * (button_size // 2) ** 2  # Área de círculo mínimo
                
                if area >= min_area:
                    # Obtener centro del contorno
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Calcular confianza basada en circularidad
                        perimeter = cv2.arcLength(largest_contour, True)
                        if perimeter > 0:
                            circularity = 4 * np.pi * area / (perimeter * perimeter)
                            confidence = min(1.0, circularity * 1.5)
                            
                            return TableElement(
                                element_type="button",
                                position=(cx, cy),
                                confidence=confidence,
                                size=(int(np.sqrt(area)), int(np.sqrt(area))),
                                color=button_color
                            )
            
        except Exception as e:
            print(f"[Table Detector] Error detectando botón: {e}")
        
        return None
    
    def _detect_player_positions(self, cv_image: np.ndarray) -> List[TableElement]:
        """Detectar posiciones de jugadores"""
        
        player_elements = []
        
        try:
            # Detectar círculos (avatars de jugadores)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar desenfoque
            blurred = cv2.medianBlur(gray, 5)
            
            # Detectar círculos usando HoughCircles
            circles = cv2.HoughCircles(
                blurred,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=50,
                param1=50,
                param2=30,
                minRadius=15,
                maxRadius=40
            )
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                
                for i, circle in enumerate(circles[0, :]):
                    x, y, radius = circle
                    
                    # Verificar si es una posición de jugador (no botón)
                    # El botón se detecta por separado
                    
                    # Obtener color promedio en el círculo
                    mask = np.zeros(cv_image.shape[:2], dtype=np.uint8)
                    cv2.circle(mask, (x, y), radius, 255, -1)
                    
                    mean_color = cv2.mean(cv_image, mask=mask)[:3]
                    
                    player_elements.append(TableElement(
                        element_type="player",
                        position=(x, y),
                        confidence=0.8,
                        size=(radius*2, radius*2),
                        color=tuple(map(int, mean_color))
                    ))
            
        except Exception as e:
            print(f"[Table Detector] Error detectando jugadores: {e}")
        
        return player_elements
    
    def _detect_pot_area(self, cv_image: np.ndarray) -> Optional[TableElement]:
        """Detectar área del pot"""
        
        try:
            # Buscar texto o área brillante en el centro de la mesa
            height, width = cv_image.shape[:2]
            
            # Región central donde normalmente está el pot
            center_x, center_y = width // 2, height // 2
            pot_region_size = 150
            
            # Extraer región del pot
            x1 = max(0, center_x - pot_region_size // 2)
            y1 = max(0, center_y - pot_region_size // 2)
            x2 = min(width, center_x + pot_region_size // 2)
            y2 = min(height, center_y + pot_region_size // 2)
            
            pot_region = cv_image[y1:y2, x1:x2]
            
            # Buscar áreas brillantes (el pot suele estar resaltado)
            gray_region = cv2.cvtColor(pot_region, cv2.COLOR_BGR2GRAY)
            _, bright_mask = cv2.threshold(gray_region, 200, 255, cv2.THRESH_BINARY)
            
            # Verificar si hay suficiente área brillante
            bright_area = cv2.countNonZero(bright_mask)
            total_area = pot_region.shape[0] * pot_region.shape[1]
            
            if bright_area / total_area > 0.1:  # Al menos 10% brillante
                # Encontrar contorno del área brillante
                contours, _ = cv2.findContours(bright_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    
                    # Ajustar coordenadas a la imagen completa
                    abs_x = x1 + x + w // 2
                    abs_y = y1 + y + h // 2
                    
                    return TableElement(
                        element_type="pot",
                        position=(abs_x, abs_y),
                        confidence=0.7,
                        size=(w, h),
                        color=self.platform_colors.get(self.platform, {}).get("pot_color", (0, 215, 255))
                    )
            
        except Exception as e:
            print(f"[Table Detector] Error detectando pot: {e}")
        
        return None
    
    def _detect_cards_areas(self, cv_image: np.ndarray) -> List[TableElement]:
        """Detectar áreas donde están las cartas"""
        
        card_areas = []
        
        try:
            # Áreas comunes para cartas:
            # 1. Cartas del héroe (abajo en el centro)
            # 2. Cartas comunitarias (centro de la mesa)
            
            height, width = cv_image.shape[:2]
            
            # Área para cartas del héroe
            hero_cards_area = TableElement(
                element_type="hero_cards",
                position=(width // 2, int(height * 0.85)),
                confidence=0.9,
                size=(200, 100),
                color=(255, 255, 255)  # Blanco para cartas
            )
            card_areas.append(hero_cards_area)
            
            # Área para cartas comunitarias
            community_cards_area = TableElement(
                element_type="community_cards",
                position=(width // 2, height // 2),
                confidence=0.9,
                size=(300, 100),
                color=(255, 255, 255)
            )
            card_areas.append(community_cards_area)
            
        except Exception as e:
            print(f"[Table Detector] Error detectando áreas de cartas: {e}")
        
        return card_areas
    
    def _detect_action_buttons(self, cv_image: np.ndarray) -> List[TableElement]:
        """Detectar botones de acción (Fold, Call, Raise)"""
        
        buttons = []
        
        try:
            # Los botones de acción suelen estar en la parte inferior