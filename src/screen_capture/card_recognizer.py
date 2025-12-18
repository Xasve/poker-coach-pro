"""
Archivo: card_recognizer.py
Ruta: src/screen_capture/card_recognizer.py
Sistema de reconocimiento de cartas de poker usando template matching
"""

import cv2
import numpy as np
from PIL import Image
import os
import json
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time

@dataclass
class Card:
    """Estructura para representar una carta de poker"""
    rank: str  # A, K, Q, J, T, 9-2
    suit: str  # h, d, c, s (hearts, diamonds, clubs, spades)
    confidence: float  # 0.0 - 1.0
    position: Tuple[int, int]  # (x, y)
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def to_dict(self):
        return {
            'rank': self.rank,
            'suit': self.suit,
            'confidence': self.confidence,
            'position': self.position
        }

class CardSuit(Enum):
    """Palos de las cartas"""
    HEARTS = 'h'
    DIAMONDS = 'd'
    CLUBS = 'c'
    SPADES = 's'

class CardRank(Enum):
    """Valores de las cartas"""
    ACE = 'A'
    KING = 'K'
    QUEEN = 'Q'
    JACK = 'J'
    TEN = 'T'
    NINE = '9'
    EIGHT = '8'
    SEVEN = '7'
    SIX = '6'
    FIVE = '5'
    FOUR = '4'
    THREE = '3'
    TWO = '2'

class CardRecognizer:
    """
    Sistema de reconocimiento de cartas de poker
    Usa template matching con OpenCV para detectar cartas
    """
    
    def __init__(self, platform: str = "ggpoker"):
        """
        Inicializar reconocedor de cartas
        
        Args:
            platform: Plataforma ("ggpoker" o "pokerstars")
        """
        self.platform = platform.lower()
        self.templates = self._load_card_templates()
        self.template_size = (71, 96)  # Tamaño estándar de cartas GG Poker
        self.confidence_threshold = 0.75
        self.min_contour_area = 500
        
        # Estadísticas
        self.stats = {
            'cards_detected': 0,
            'recognition_attempts': 0,
            'success_rate': 0.0,
            'avg_confidence': 0.0
        }
        
        print(f"[Card Recognizer] Inicializado para {self.platform.upper()}")
        
    def _load_card_templates(self) -> Dict:
        """
        Cargar templates de cartas desde archivos
        En producción, estos estarían en data/card_templates/
        """
        
        # Mapeo de colores por plataforma
        platform_colors = {
            "ggpoker": {
                "hearts": (0, 0, 255),    # Rojo
                "diamonds": (0, 0, 255),  # Rojo
                "clubs": (0, 0, 0),       # Negro
                "spades": (0, 0, 0)       # Negro
            },
            "pokerstars": {
                "hearts": (255, 0, 0),    # Rojo
                "diamonds": (255, 0, 0),  # Rojo
                "clubs": (0, 0, 0),       # Negro
                "spades": (0, 0, 0)       # Negro
            }
        }
        
        # Crear templates básicos (en producción se cargarían desde imágenes)
        templates = {}
        
        # Valores y palos
        ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        suits = ['h', 'd', 'c', 's']
        
        for rank in ranks:
            for suit in suits:
                card_key = f"{rank}{suit}"
                templates[card_key] = {
                    'rank': rank,
                    'suit': suit,
                    'color': platform_colors.get(self.platform, {}).get(
                        'hearts' if suit in ['h', 'd'] else 'clubs', 
                        (0, 0, 0)
                    )
                }
        
        return templates
    
    def recognize_cards(self, image: Image.Image, card_count: int = 2) -> List[Card]:
        """
        Reconocer cartas en una imagen
        
        Args:
            image: PIL Image a analizar
            card_count: Número esperado de cartas (2 para hole cards)
            
        Returns:
            Lista de objetos Card detectados
        """
        start_time = time.time()
        self.stats['recognition_attempts'] += 1
        
        try:
            # Convertir PIL Image a OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocesar imagen
            processed = self._preprocess_image(cv_image)
            
            # Encontrar contornos de cartas
            card_contours = self._find_card_contours(processed)
            
            # Si no encontramos contornos, usar detección por color
            if len(card_contours) < card_count:
                card_contours = self._find_cards_by_color(cv_image)
            
            # Ordenar contornos de izquierda a derecha
            card_contours = sorted(card_contours, key=lambda c: cv2.boundingRect(c)[0])
            
            # Procesar cada contorno de carta
            detected_cards = []
            for i, contour in enumerate(card_contours[:card_count]):  # Limitar al número esperado
                try:
                    # Extraer región de la carta
                    x, y, w, h = cv2.boundingRect(contour)
                    card_region = cv_image[y:y+h, x:x+w]
                    
                    # Reconocer carta
                    card = self._recognize_single_card(card_region)
                    if card:
                        card.position = (x + w//2, y + h//2)  # Centro de la carta
                        detected_cards.append(card)
                        
                except Exception as e:
                    print(f"[Card Recognizer] Error procesando carta {i}: {e}")
                    continue
            
            # Actualizar estadísticas
            self._update_stats(detected_cards, time.time() - start_time)
            
            return detected_cards
            
        except Exception as e:
            print(f"[Card Recognizer] Error en reconocimiento: {e}")
            return []
    
    def _preprocess_image(self, cv_image: np.ndarray) -> np.ndarray:
        """Preprocesar imagen para detección de contornos"""
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar desenfoque para reducir ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detectar bordes
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilatar bordes para conectar líneas rotas
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        return dilated
    
    def _find_card_contours(self, processed_image: np.ndarray) -> List:
        """Encontrar contornos que podrían ser cartas"""
        
        # Encontrar contornos
        contours, _ = cv2.findContours(
            processed_image, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filtrar contornos por área y relación de aspecto
        card_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtrar por área mínima
            if area < self.min_contour_area:
                continue
            
            # Obtener bounding rect
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calcular relación de aspecto (cartas ~ 0.7-0.8)
            aspect_ratio = w / h if h > 0 else 0
            
            # Filtrar por relación de aspecto de carta
            if 0.6 <= aspect_ratio <= 0.9:
                card_contours.append(contour)
        
        return card_contours
    
    def _find_cards_by_color(self, cv_image: np.ndarray) -> List:
        """Buscar cartas por detección de color"""
        
        # Convertir a HSV para mejor detección de color
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        # Definir rangos de color para cartas (rojizo/marron)
        lower_color = np.array([0, 20, 20])
        upper_color = np.array([20, 255, 255])
        
        # Crear máscara de color
        color_mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Encontrar contornos en la máscara
        contours, _ = cv2.findContours(
            color_mask, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        return contours
    
    def _recognize_single_card(self, card_image: np.ndarray) -> Optional[Card]:
        """Reconocer una sola carta"""
        
        try:
            # Redimensionar a tamaño estándar para matching
            resized = cv2.resize(card_image, self.template_size)
            
            # Convertir a escala de grises para template matching
            gray_card = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            
            # Intentar reconocer el valor (rank)
            rank, rank_confidence = self._recognize_rank(gray_card)
            
            # Intentar reconocer el palo (suit)
            suit, suit_confidence = self._recognize_suit(card_image)
            
            # Calcular confianza promedio
            confidence = (rank_confidence + suit_confidence) / 2
            
            if confidence >= self.confidence_threshold:
                return Card(
                    rank=rank,
                    suit=suit,
                    confidence=confidence,
                    position=(0, 0)  # Se actualizará después
                )
            
        except Exception as e:
            print(f"[Card Recognizer] Error reconociendo carta: {e}")
        
        return None
    
    def _recognize_rank(self, gray_card: np.ndarray) -> Tuple[str, float]:
        """Reconocer el valor de la carta (rank)"""
        
        # Método simplificado basado en forma
        # En producción usaríamos templates o ML
        
        # Detectar esquinas o patrones específicos
        edges = cv2.Canny(gray_card, 50, 150)
        
        # Contar píxeles de bordes (proxy para complejidad)
        edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        
        # Mapear densidad a valores de carta (simplificado)
        if edge_density < 0.1:
            rank = 'A'  # As simple
            confidence = 0.8
        elif edge_density < 0.15:
            rank = 'K'  # Rey
            confidence = 0.7
        elif edge_density < 0.2:
            rank = 'Q'  # Reina
            confidence = 0.7
        elif edge_density < 0.25:
            rank = 'J'  # Jota
            confidence = 0.6
        else:
            # Para números, estimar basado en densidad
            density_to_number = {
                0.25: 'T', 0.3: '9', 0.35: '8', 0.4: '7',
                0.45: '6', 0.5: '5', 0.55: '4', 0.6: '3', 0.65: '2'
            }
            
            # Encontrar el número más cercano
            closest = min(density_to_number.keys(), key=lambda x: abs(x - edge_density))
            rank = density_to_number[closest]
            confidence = 0.6 - abs(closest - edge_density) * 2
        
        return rank, max(0.3, min(0.9, confidence))
    
    def _recognize_suit(self, card_image: np.ndarray) -> Tuple[str, float]:
        """Reconocer el palo de la carta (suit)"""
        
        # Convertir a HSV para detección de color
        hsv = cv2.cvtColor(card_image, cv2.COLOR_BGR2HSV)
        
        # Definir rangos HSV para rojo (corazones y diamantes)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Crear máscaras para rojo
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Contar píxeles rojos
        red_pixels = cv2.countNonZero(mask_red)
        total_pixels = card_image.shape[0] * card_image.shape[1]
        red_ratio = red_pixels / total_pixels
        
        # Si hay suficiente rojo, es corazón o diamante
        if red_ratio > 0.05:
            # Diferenciar entre corazones y diamantes por forma
            # Simplificado: corazón si hay más rojo en la parte superior
            top_half = mask_red[:mask_red.shape[0]//2, :]
            bottom_half = mask_red[mask_red.shape[0]//2:, :]
            
            top_red = cv2.countNonZero(top_half)
            bottom_red = cv2.countNonZero(bottom_half)
            
            if top_red > bottom_red * 1.5:
                suit = 'h'  # Corazones (más rojo arriba)
            else:
                suit = 'd'  # Diamantes
            
            confidence = min(0.9, red_ratio * 10)
        else:
            # Negro: tréboles o picas
            # Diferenciar por forma simplificada
            gray = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # Tréboles tienden a tener más bordes
            edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
            
            if edge_density > 0.3:
                suit = 'c'  # Tréboles
            else:
                suit = 's'  # Picas
            
            confidence = 0.6
        
        return suit, confidence
    
    def _update_stats(self, detected_cards: List[Card], processing_time: float):
        """Actualizar estadísticas"""
        
        if detected_cards:
            self.stats['cards_detected'] += len(detected_cards)
            
            # Calcular confianza promedio
            avg_confidence = sum(c.confidence for c in detected_cards) / len(detected_cards)
            
            # Actualizar promedio móvil
            old_avg = self.stats['avg_confidence']
            self.stats['avg_confidence'] = 0.1 * avg_confidence + 0.9 * old_avg if old_avg > 0 else avg_confidence
            
            # Calcular tasa de éxito
            self.stats['success_rate'] = (
                self.stats['cards_detected'] / 
                (self.stats['recognition_attempts'] * 2) * 100  # 2 cartas por intento
            )
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas"""
        return {
            'cards_detected': self.stats['cards_detected'],
            'recognition_attempts': self.stats['recognition_attempts'],
            'success_rate': f"{self.stats['success_rate']:.1f}%",
            'avg_confidence': f"{self.stats['avg_confidence']:.2f}",
            'platform': self.platform
        }
    
    def save_detection_image(self, original: Image.Image, detected_cards: List[Card], 
                           filename: str = "card_detection.png"):
        """Guardar imagen con detecciones marcadas"""
        
        try:
            # Convertir a OpenCV
            cv_image = cv2.cvtColor(np.array(original), cv2.COLOR_RGB2BGR)
            
            # Dibujar bounding boxes y texto
            for card in detected_cards:
                if card.position[0] > 0:  # Si tiene posición válida
                    # Dibujar círculo en el centro
                    cv2.circle(cv_image, card.position, 10, (0, 255, 0), 2)
                    
                    # Añadir texto con la carta
                    text = f"{card.rank}{card.suit} ({card.confidence:.2f})"
                    cv2.putText(
                        cv_image, text,
                        (card.position[0] + 15, card.position[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2
                    )
            
            # Guardar imagen
            cv2.imwrite(filename, cv_image)
            print(f"[Card Recognizer] Imagen guardada: {filename}")
            
        except Exception as e:
            print(f"[Card Recognizer] Error guardando imagen: {e}")

# Función de prueba
def test_card_recognition():
    """Probar reconocimiento de cartas"""
    
    print("🎴 Probando reconocimiento de cartas...")
    
    # Crear una imagen de prueba con "cartas" simuladas
    from PIL import Image, ImageDraw
    import random
    
    # Crear imagen de prueba
    test_image = Image.new('RGB', (800, 600), color=(53, 101, 77))  # Fondo verde de mesa
    
    draw = ImageDraw.Draw(test_image)
    
    # Dibujar dos "cartas" simuladas
    card_positions = [(200, 400), (350, 400)]
    card_size = (100, 140)
    
    for i, (x, y) in enumerate(card_positions):
        # Dibujar rectángulo de carta
        draw.rectangle([x, y, x + card_size[0], y + card_size[1]], 
                      fill=(255, 255, 255), outline=(0, 0, 0), width=3)
        
        # Añadir "valor" y "palo" simulados
        draw.text((x + 20, y + 20), "A", fill=(255, 0, 0), font_size=30)
        draw.text((x + 20, y + 60), "♥", fill=(255, 0, 0), font_size=30)
    
    print("🖼️  Imagen de prueba creada")
    
    # Probar reconocedor
    recognizer = CardRecognizer(platform="ggpoker")
    cards = recognizer.recognize_cards(test_image, card_count=2)
    
    print(f"\n🔍 Resultados del reconocimiento:")
    for i, card in enumerate(cards):
        print(f"  Carta {i+1}: {card.rank}{card.suit} (confianza: {card.confidence:.2f})")
    
    # Mostrar estadísticas
    stats = recognizer.get_stats()
    print(f"\n📊 Estadísticas: {stats}")
    
    # Guardar imagen con detecciones
    recognizer.save_detection_image(test_image, cards, "test_card_detection.png")
    
    return cards

if __name__ == "__main__":
    test_card_recognition()