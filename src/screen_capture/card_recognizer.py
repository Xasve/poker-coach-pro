"""
card_recognizer.py - Sistema de reconocimiento de cartas por template matching
Reconoce cartas del hero y mesa en GG Poker y PokerStars
"""

import cv2
import numpy as np
import os
import time
import random
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import logging

from ..utils.image_utils import ImageUtils
from ..quality.quality_checker import QualityChecker

@dataclass
class Card:
    """Clase que representa una carta de poker"""
    rank: str  # 'A', 'K', 'Q', 'J', '10', '9', ..., '2'
    suit: str  # 's' (spades), 'h' (hearts), 'd' (diamonds), 'c' (clubs)
    confidence: float  # 0.0 a 1.0
    position: Tuple[int, int]  # Posición en la imagen
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def to_poker_format(self) -> str:
        """Formato estándar de poker (ej: 'Ah' para Ace of hearts)"""
        return f"{self.rank}{self.suit}"

class CardRecognizer:
    """Sistema principal de reconocimiento de cartas"""
    
    def __init__(self, platform: str = "ggpoker", stealth_level: str = "MEDIUM"):
        """
        Inicializar reconocedor de cartas
        
        Args:
            platform: 'ggpoker' o 'pokerstars'
            stealth_level: Nivel de stealth (MINIMUM, MEDIUM, MAXIMUM)
        """
        self.platform = platform.lower()
        self.stealth_level = stealth_level
        self.logger = logging.getLogger(__name__)
        self.quality_checker = QualityChecker()
        
        # Umbrales de confianza por nivel de stealth
        self.confidence_thresholds = {
            "MINIMUM": 0.80,
            "MEDIUM": 0.85,
            "MAXIMUM": 0.90
        }
        
        # Cargar templates de cartas
        self.templates = self._load_card_templates()
        self.logger.info(f"CardRecognizer inicializado para {platform}")
        
        # Estadísticas
        self.stats = {
            "total_recognitions": 0,
            "successful_recognitions": 0,
            "avg_confidence": 0.0,
            "avg_processing_time": 0.0
        }
    
    def _load_card_templates(self) -> Dict[str, np.ndarray]:
        """
        Cargar templates de cartas desde el directorio data/card_templates/
        
        Returns:
            Diccionario con templates (clave: 'Ah', 'Kd', etc.)
        """
        templates = {}
        template_dir = "data/card_templates"
        
        if not os.path.exists(template_dir):
            self.logger.warning(f"Directorio de templates no encontrado: {template_dir}")
            # Crear directorio si no existe
            os.makedirs(template_dir, exist_ok=True)
            # En una implementación real, aquí se generarían los templates
            return templates
        
        ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        suits = ['s', 'h', 'd', 'c']  # spades, hearts, diamonds, clubs
        
        for rank in ranks:
            for suit in suits:
                card_name = f"{rank}{suit}"
                template_path = os.path.join(template_dir, f"{card_name}.png")
                
                if os.path.exists(template_path):
                    try:
                        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                        if template is not None:
                            # Redimensionar a tamaño estándar
                            template = cv2.resize(template, (80, 120))
                            templates[card_name] = template
                            self.logger.debug(f"Template cargado: {card_name}")
                        else:
                            self.logger.warning(f"No se pudo cargar template: {card_name}")
                    except Exception as e:
                        self.logger.error(f"Error cargando template {card_name}: {e}")
                else:
                    self.logger.debug(f"Template no encontrado: {card_name}")
        
        self.logger.info(f"Templates cargados: {len(templates)}/52")
        return templates
    
    def recognize_cards_in_region(self, screenshot: np.ndarray, 
                                 region_config: Dict) -> List[Card]:
        """
        Reconocer cartas en una región específica de la pantalla
        
        Args:
            screenshot: Captura de pantalla completa
            region_config: Configuración de región (de JSON config)
            
        Returns:
            Lista de cartas reconocidas
        """
        start_time = time.time()
        
        # Aplicar randomización de timing según nivel de stealth
        self._apply_stealth_delay()
        
        # Extraer región de interés
        roi = self._extract_roi(screenshot, region_config)
        
        if roi is None or roi.size == 0:
            self.logger.warning("Región de interés vacía o inválida")
            return []
        
        # Preprocesar imagen
        processed_roi = self._preprocess_image(roi)
        
        # Detectar cartas individuales en la región
        card_images = self._detect_individual_cards(processed_roi)
        
        # Reconocer cada carta
        recognized_cards = []
        for i, card_img in enumerate(card_images):
            card = self._recognize_single_card(card_img)
            if card:
                # Ajustar posición a coordenadas de screenshot original
                card.position = self._adjust_position(card.position, region_config, i, len(card_images))
                recognized_cards.append(card)
        
        # Validar resultado
        if self._validate_recognition(recognized_cards):
            self.stats["successful_recognitions"] += 1
        
        # Actualizar estadísticas
        processing_time = time.time() - start_time
        self._update_stats(processing_time, recognized_cards)
        
        self.logger.debug(f"Reconocidas {len(recognized_cards)} cartas en {processing_time:.3f}s")
        return recognized_cards
    
    def _apply_stealth_delay(self):
        """Aplicar delay aleatorio según nivel de stealth"""
        delays = {
            "MINIMUM": (0.05, 0.15),      # 50-150ms
            "MEDIUM": (0.15, 0.30),       # 150-300ms
            "MAXIMUM": (0.25, 0.50)       # 250-500ms
        }
        
        if self.stealth_level in delays:
            min_delay, max_delay = delays[self.stealth_level]
            delay = random.uniform(min_delay, max_delay)
            time.sleep(delay)
    
    def _extract_roi(self, screenshot: np.ndarray, 
                    region_config: Dict) -> Optional[np.ndarray]:
        """
        Extraer región de interés basada en porcentajes
        
        Args:
            screenshot: Imagen completa
            region_config: Config con x1, y1, x2, y2 en porcentajes
            
        Returns:
            Región de interés recortada
        """
        try:
            h, w = screenshot.shape[:2]
            
            # Convertir porcentajes a píxeles
            x1 = int(w * region_config.get('x1', 0))
            y1 = int(h * region_config.get('y1', 0))
            x2 = int(w * region_config.get('x2', 1))
            y2 = int(h * region_config.get('y2', 1))
            
            # Asegurar límites válidos
            x1 = max(0, min(x1, w))
            x2 = max(0, min(x2, w))
            y1 = max(0, min(y1, h))
            y2 = max(0, min(y2, h))
            
            if x2 <= x1 or y2 <= y1:
                self.logger.warning(f"Región inválida: ({x1},{y1})-({x2},{y2})")
                return None
            
            roi = screenshot[y1:y2, x1:x2]
            return roi
            
        except Exception as e:
            self.logger.error(f"Error extrayendo ROI: {e}")
            return None
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocesar imagen para mejor reconocimiento
        
        Args:
            image: Imagen a preprocesar
            
        Returns:
            Imagen preprocesada
        """
        # Convertir a escala de grises
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Aplicar filtro bilateral para reducir ruido manteniendo bordes
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Aumentar contraste
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(filtered)
        
        # Umbralización adaptativa
        thresh = cv2.adaptiveThreshold(enhanced, 255, 
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        
        return thresh
    
    def _detect_individual_cards(self, roi: np.ndarray) -> List[np.ndarray]:
        """
        Detectar cartas individuales dentro de una región
        
        Args:
            roi: Región que contiene múltiples cartas
            
        Returns:
            Lista de imágenes de cartas individuales
        """
        card_images = []
        
        try:
            # Encontrar contornos
            contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, 
                                          cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Filtrar por área
                area = cv2.contourArea(contour)
                if area < 100:  # Muy pequeño para ser una carta
                    continue
                
                # Obtener rectángulo delimitador
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filtrar por relación de aspecto (cartas típicas ~2:3)
                aspect_ratio = h / w if h > 0 else 0
                if not (1.2 < aspect_ratio < 2.0):
                    continue
                
                # Extraer la carta
                card_img = roi[y:y+h, x:x+w]
                
                # Redimensionar a tamaño estándar
                card_img = cv2.resize(card_img, (80, 120))
                card_images.append(card_img)
                
        except Exception as e:
            self.logger.error(f"Error detectando cartas individuales: {e}")
        
        # Ordenar de izquierda a derecha
        card_images.sort(key=lambda img: np.mean(np.where(img > 0)[1]) 
                        if img.size > 0 else 0)
        
        return card_images
    
    def _recognize_single_card(self, card_image: np.ndarray) -> Optional[Card]:
        """
        Reconocer una carta individual usando template matching
        
        Args:
            card_image: Imagen de una sola carta
            
        Returns:
            Objeto Card reconocido o None
        """
        if card_image is None or card_image.size == 0:
            return None
        
        best_match = None
        best_confidence = 0.0
        
        for card_name, template in self.templates.items():
            try:
                # Template matching
                result = cv2.matchTemplate(card_image, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_confidence and max_val > self.confidence_thresholds.get(self.stealth_level, 0.85):
                    best_confidence = max_val
                    best_match = card_name
                    
            except Exception as e:
                self.logger.debug(f"Error en template matching para {card_name}: {e}")
                continue
        
        if best_match:
            # Extraer rank y suit del nombre
            rank = best_match[:-1]
            suit = best_match[-1]
            
            # Obtener posición aproximada
            position = (np.mean(np.where(card_image > 0)[1]), 
                       np.mean(np.where(card_image > 0)[0]))
            
            return Card(rank=rank, suit=suit, 
                       confidence=best_confidence,
                       position=position)
        
        return None
    
    def _adjust_position(self, position: Tuple[float, float],
                        region_config: Dict,
                        card_index: int,
                        total_cards: int) -> Tuple[int, int]:
        """
        Ajustar posición de la carta a coordenadas globales
        
        Args:
            position: Posición local en la ROI
            region_config: Configuración de la región
            card_index: Índice de la carta
            total_cards: Total de cartas detectadas
            
        Returns:
            Posición ajustada en coordenadas globales
        """
        # En una implementación real, esto ajustaría basado en la ROI
        # Por ahora, retornar posición aproximada
        x_offset = card_index * 30  # Espaciado aproximado entre cartas
        return (int(position[0] + x_offset), int(position[1]))
    
    def _validate_recognition(self, cards: List[Card]) -> bool:
        """
        Validar que el reconocimiento sea lógico
        
        Args:
            cards: Lista de cartas reconocidas
            
        Returns:
            True si la validación pasa
        """
        if not cards:
            return False
        
        # Verificar que no haya cartas duplicadas
        card_strings = [str(card) for card in cards]
        if len(card_strings) != len(set(card_strings)):
            self.logger.warning("Cartas duplicadas detectadas")
            return False
        
        # Verificar confianza mínima
        min_confidence = min(card.confidence for card in cards)
        if min_confidence < self.confidence_thresholds.get(self.stealth_level, 0.85):
            self.logger.warning(f"Confianza muy baja: {min_confidence:.3f}")
            return False
        
        # Verificar número de cartas (2 para hero, 0-5 para mesa)
        if not (0 <= len(cards) <= 5):
            self.logger.warning(f"Número inusual de cartas: {len(cards)}")
            return False
        
        return True
    
    def _update_stats(self, processing_time: float, cards: List[Card]):
        """Actualizar estadísticas de reconocimiento"""
        self.stats["total_recognitions"] += 1
        
        if cards:
            avg_conf = np.mean([card.confidence for card in cards])
            self.stats["avg_confidence"] = (
                self.stats["avg_confidence"] * (self.stats["total_recognitions"] - 1) + avg_conf
            ) / self.stats["total_recognitions"]
        
        self.stats["avg_processing_time"] = (
            self.stats["avg_processing_time"] * (self.stats["total_recognitions"] - 1) + processing_time
        ) / self.stats["total_recognitions"]
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas actuales"""
        success_rate = (
            (self.stats["successful_recognitions"] / self.stats["total_recognitions"] * 100)
            if self.stats["total_recognitions"] > 0 else 0
        )
        
        return {
            **self.stats,
            "success_rate": success_rate,
            "templates_loaded": len(self.templates)
        }
    
    def reset_stats(self):
        """Reiniciar estadísticas"""
        self.stats = {
            "total_recognitions": 0,
            "successful_recognitions": 0,
            "avg_confidence": 0.0,
            "avg_processing_time": 0.0
        }


# Clase auxiliar para manejo de imágenes
class ImageUtils:
    """Utilidades para procesamiento de imágenes"""
    
    @staticmethod
    def save_debug_image(image: np.ndarray, filename: str, 
                        cards: List[Card] = None):
        """
        Guardar imagen para debugging
        
        Args:
            image: Imagen a guardar
            filename: Nombre del archivo
            cards: Lista de cartas para dibujar (opcional)
        """
        debug_dir = "debug_images"
        os.makedirs(debug_dir, exist_ok=True)
        
        # Convertir a BGR si es necesario
        if len(image.shape) == 2:
            debug_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            debug_img = image.copy()
        
        # Dibujar cartas reconocidas
        if cards:
            for card in cards:
                x, y = map(int, card.position)
                cv2.putText(debug_img, str(card), (x, y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                           (0, 255, 0), 2)
        
        # Guardar imagen
        cv2.imwrite(os.path.join(debug_dir, filename), debug_img)
    
    @staticmethod
    def show_image(image: np.ndarray, title: str = "Image"):
        """Mostrar imagen (solo para debugging)"""
        cv2.imshow(title, image)
        cv2.waitKey(1)
        cv2.destroyAllWindows()


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Inicializar reconocedor
    recognizer = CardRecognizer(platform="ggpoker", stealth_level="MEDIUM")
    
    # Simular captura (en producción esto vendría del screen_capture)
    # test_image = cv2.imread("test_screenshot.png")
    
    # Configuración de región de ejemplo
    region_config = {
        "x1": 0.45,
        "y1": 0.75,
        "x2": 0.55,
        "y2": 0.85
    }
    
    # Ejemplo de reconocimiento
    # cards = recognizer.recognize_cards_in_region(test_image, region_config)
    
    print("CardRecognizer listo para usar")
    print("Estadísticas iniciales:", recognizer.get_stats())